import openai
import logging
import json
import pandas as pd
import re
import numpy as np
import emoji
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
from sklearn.cluster import DBSCAN
from typing import List, Dict, Tuple
import warnings
import nltk
from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from tqdm.auto import tqdm
import time
from datetime import datetime
from bertopic.representation import OpenAI
from bertopic import BERTopic
import tiktoken

warnings.filterwarnings('ignore')


class TopicModelingPipelineBertopic:
    def __init__(self, 
                 embedding_model: str = 'BAAI/bge-base-en-v1.5',
                 eps: float = 0.5,
                 min_samples: int = 5,
                 n_neighbors: int = 15,
                 n_components: int = 5,
                 nr_topics=25,
                 random_state: int = 42,
                 openai_api_key: str =None,
                 log_level: str = 'INFO'):
        """
        Initialize the topic modeling pipeline using BERTopic with DBSCAN clustering.
        
        Args:
            embedding_model: Name of the sentence-transformers model to use
            eps: DBSCAN eps parameter
            min_samples: DBSCAN min_samples parameter
            n_neighbors: UMAP n_neighbors parameter
            n_components: UMAP n_components parameter
            random_state: Random seed for reproducibility
            openai_api_key: OpenAI API key for topic representation
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Set up logging
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Initializing TopicModelingPipeline with model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize UMAP for dimensionality reduction
        self.umap_model = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=n_components,
            metric='cosine',
            random_state=random_state
        )
        
        # Initialize DBSCAN for clustering
        self.dbscan_model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric='euclidean',
            n_jobs=-1
        )
        
        # Initialize OpenAI client and tokenizer
        if openai_api_key:
            self.client = openai.OpenAI(api_key=openai_api_key)
            self.tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")      
            
            self.representation_model = OpenAI(
                client=self.client,
                model="gpt-4o-mini",
                delay_in_seconds=2,
                chat=True,
                doc_length=100,
                tokenizer=self.tokenizer,
                prompt=self._get_user_prompt(),
                nr_docs=4
            )
        else:
            self.representation_model = None
        
        # Initialize BERTopic with custom components
        self.topic_model = BERTopic(
            embedding_model=embedding_model,
            umap_model=self.umap_model,
            hdbscan_model=self.dbscan_model,
            n_gram_range=(1, 3),
            representation_model=self.representation_model,
            calculate_probabilities=False,
            verbose=True,
            top_n_words=10,
            nr_topics=nr_topics
        )
        
        self.logger.info("Pipeline initialized successfully")

    def setup_logging(self, log_level: str):
        """Set up logging configuration"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'logs/topic_modeling_{timestamp}.log'
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
    def get_topics(self):
        return self.topic_model.topics_

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the input data."""
        self.logger.info("Starting data preprocessing")
        total_rows = len(df)

        if 'comment' not in df.columns:
            self.logger.error("DataFrame missing 'comment' column")
            raise ValueError("The DataFrame must contain a column named 'comment'.")

        df = df[df['comment'].notna()]
        self.logger.debug(f"Removed {total_rows - len(df)} rows with null comments")

        # Preprocessing steps
        df['comment'] = df['comment'].apply(lambda x: x.strip() if isinstance(x, str) else '')
        df = df[df['comment'] != ""]

        # Remove duplicates
        initial_len = len(df)
        df = df.drop_duplicates(subset='comment', keep='first')
        self.logger.debug(f"Removed {initial_len - len(df)} duplicate comments")

        # Remove short comments
        df['comment_length'] = df['comment'].str.len()
        df = df[df['comment_length'] > 20]
        self.logger.debug(f"Removed rows with short comments. Remaining rows: {len(df)}")

        df = df.reset_index(drop=True)
        self.logger.info(f"Preprocessing complete. Final dataset size: {len(df)} comments")
        return df

    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for the input texts."""

        self.logger.info("Generating embeddings")
        self.logger.info(f"Number of input texts: {len(texts)}")
        
        start_time = time.time()
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32
        )
        duration = time.time() - start_time
        self.logger.info(f"Embeddings generated in {duration:.2f} seconds")

        # Validate embeddings
        if embeddings.shape[0] != len(texts):
            raise ValueError(f"Embeddings count ({embeddings.shape[0]}) does not match document count ({len(texts)}).")
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D NumPy array.")

        self.logger.info(f"Embeddings shape: {embeddings.shape}")
        return embeddings


    
    def save_embeddings(self, embeddings: np.ndarray, save_folder: str = 'data'):
        """Saves embeddings in the file"""
        self.logger.info(f"Saving embeddings to {save_folder}")
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, 
                               f'embeddings_{self.embedding_model_name.replace("/", "_").lower()}.npy')
        
        with open(save_path, 'wb') as f:
            np.save(f, embeddings)
        self.logger.info(f"Embeddings saved to {save_path}")
        
    
    def _get_user_prompt(self) -> str:
        """Helper method to get the formatted prompt for topic generation."""
        delimiter = "###"
        return f"""Based on the following social media comments and their associated keywords, generate one topic label according to the guideline.

1. The topic label must capture the core theme connecting the provided keywords and content.
2. Be precise but avoid overcomplicating the label. Use 2-5 words.
3. Ensure the label reflects the subject matter indicated by the keywords and documents, without being generic or overly simplistic.
4. Avoid inserting personal bias or emotionally charged language into the labels.

Provide the output strictly in plain text format.

Social Media Comments:
{delimiter}
[DOCUMENTS]
{delimiter}

Keywords:
{delimiter}
[KEYWORDS]
{delimiter}

Carefully analyze both the comments and keywords to determine appropriate topic labels. Ensure the labels are precise, contextually relevant, and reflect the primary themes present in the data."""

    def fit_transform(self, df: pd.DataFrame, embeddings: np.ndarray = None) -> Tuple[pd.DataFrame, Dict]:
        """Run the complete topic modeling pipeline."""
        start_time = time.time()
        self.logger.info("Starting topic modeling pipeline")

        # Preprocess data
        df = self.preprocess_data(df)
        texts = df['comment'].tolist()

        # Ensure we have valid texts
        if not texts:
            raise ValueError("No valid comments found after preprocessing.")

        # Generate embeddings if not provided
        if embeddings is None:
            self.logger.info("No embeddings were passed, generating embeddings and saving them")
            embeddings = self.generate_embeddings(texts)

        # Validate embeddings
        self.logger.info(f"Number of texts: {len(texts)}")
        self.logger.info(f"Shape of embeddings: {embeddings.shape}")
        if embeddings.shape[0] != len(texts):
            raise ValueError(f"Embeddings count ({embeddings.shape[0]}) does not match document count ({len(texts)}).")
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D NumPy array.")

        # Fit BERTopic model
        self.logger.info("Fitting BERTopic model")
        topics, probs = self.topic_model.fit_transform(texts, embeddings)

        # Get topic information
        topic_info = self.topic_model.get_topic_info()

        # Add results to DataFrame
        df['topic_cluster'] = topics
        df['topic_label'] = df['topic_cluster'].map(
            {topic: info for topic, info in self.topic_model.topic_labels_.items()}
        )

        # Prepare topic info dictionary
        topic_info_dict = {
            'labels': [info for topic, info in sorted(self.topic_model.topic_labels_.items()) if topic != -1],
            'keywords': [list(zip(*self.topic_model.get_topic(i)))[0] for i in range(len(topic_info) - 1)],  # Exclude outlier topic
            'size': topic_info['Count'].tolist()[1:]  # Exclude outlier topic
        }

        duration = time.time() - start_time
        self.logger.info(f"Pipeline completed in {duration:.2f} seconds")

        # Log topic distribution
        for topic_idx, (label, size) in enumerate(zip(topic_info_dict['labels'], topic_info_dict['size'])):
            self.logger.info(f"Topic {topic_idx}: {label} ({size} documents)")
            self.logger.debug(f"Keywords: {', '.join(topic_info_dict['keywords'][topic_idx][:10])}")

        return df, topic_info_dict, self.topic_model

    
    def reduce_topics(self, df, nr_topics=20):
        texts = df['comment'].tolist()
        self.topic_model.reduce_topics(texts, nr_topics=nr_topics)
        

    def save_model(self, save_path: str = 'models'):
        """Save the BERTopic model to disk."""
        self.logger.info(f"Saving model to {save_path}")
        os.makedirs(save_path, exist_ok=True)
        
        try:
            # Save BERTopic model
            self.topic_model.save(os.path.join(save_path, 'bertopic_model'))
            
            # Save configuration
            config = {
                'embedding_model': self.embedding_model_name,
                'umap_params': self.umap_model.get_params(),
                'dbscan_params': self.dbscan_model.get_params()
            }
            with open(os.path.join(save_path, 'config.json'), 'w') as f:
                json.dump(config, f)
                
            self.logger.info("Model saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            raise

    @classmethod
    def load_model(cls, load_path: str = 'models') -> 'TopicModelingPipelineBertopic':
        """Load a saved BERTopic model from disk."""
        logger = logging.getLogger(__name__)
        logger.info(f"Loading model from {load_path}")
        
        try:
            # Load configuration
            with open(os.path.join(load_path, 'config.json'), 'r') as f:
                config = json.load(f)
            
            # Initialize pipeline with saved config
            pipeline = cls(
                embedding_model=config['embedding_model']
            )
            
            # Load BERTopic model
            pipeline.topic_model = BERTopic.load(os.path.join(load_path, 'bertopic_model'))
            
            logger.info("Model loaded successfully")
            return pipeline
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise


def create_topics(csvpath: str, openai_key: str):
    pipeline = TopicModelingPipelineBertopic(embedding_model='BAAI/bge-base-en-v1.5', 
                                             eps=0.3, 
                                             min_samples=100, 
                                             nr_topics=25, 
                                             log_level='INFO',
                                             openai_api_key=openai_key
                                             )
    
    # TODO: retrieve data the other way, e.g. through database
    df = pd.read_csv(csvpath)
    #embeddings = np.load('data/embeddings_comments.npy')
    df, topic_info_dict, topic_model = pipeline.fit_transform(df)
    topic_model.save("models", serialization="safetensors", save_ctfidf=True, save_embedding_model='BAAI/bge-base-en-v1.5')
    
    # for outliers elimination
    new_topics = topic_model.reduce_outliers(df['comment'].tolist(), df['topic_cluster'].tolist())
    df['topic_cluster'] = new_topics

    # The first one is always outlier label, keeping all except this one
    topic_labels = list(map(lambda x: x.split('_')[-1], topic_model.topic_labels_.values()))[1:]

    #TODO: save topics



if __name__ == "__main__":
    csvpath = 'CSV_data/fulldata.csv'
    openai_key = '---ADD API KEY----'
    create_topics(csvpath, openai_key)
