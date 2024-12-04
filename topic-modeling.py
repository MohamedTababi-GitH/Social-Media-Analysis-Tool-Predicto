from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
import pandas as pd
import logging
import re
import tqdm
from pathlib import Path

# Topics related
from bertopic import BERTopic
from bertopic.representation import TextGeneration
from transformers import AutoTokenizer, pipeline
from ctransformers import AutoModelForCausalLM
import torch
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN

# Text preprocessing
from nltk.corpus import stopwords
import nltk
import spacy
import torch
import emoji

# Database connection
import sqlite3

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
tqdm.pandas()


@dataclass
class ModelConfig:
    embedding_model: str
    min_topic_size: int
    nr_topics: int
    min_cluster_size: int
    representation_model: Optional[TextGeneration] = None
    calculate_probabilities: bool = True
    verbose: bool = True

class TextPreprocessor:
    def __init__(self, batch_size: int = 1000):
        self.nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])
        self.stop_words = set(stopwords.words('english'))
        self.batch_size = batch_size
        
    def clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = emoji.demojize(text)
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)
        text = re.sub(r"@\w+|#\w+", "", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.lower().strip()
    
    def tokenize_and_lemmatize(self, text: str) -> str:
        tokens = nltk.word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        doc = self.nlp(" ".join(tokens))
        return " ".join([token.lemma_ for token in doc 
                        if not token.is_punct and not token.is_space])
    
    def process_batch(self, texts: List[str]) -> List[str]:
        return [self.tokenize_and_lemmatize(self.clean_text(text)) 
                for text in texts]
    
    def process_series(self, series: pd.Series) -> pd.Series:
        batches = [series[i:i + self.batch_size] 
                  for i in range(0, len(series), self.batch_size)]
        processed = []
        for batch in tqdm(batches, desc="Processing text"):
            processed.extend(self.process_batch(batch))
        return pd.Series(processed, index=series.index)


class TopicModelDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def fetch_comments(self, table_name: str) -> pd.DataFrame:
        with self.connect() as conn:
            return pd.read_sql_query(
                f"SELECT id, comment FROM {table_name}", conn)
    
    def update_topics(self, df: pd.DataFrame, table_name: str):
        with self.connect() as conn:
            temp_table = f"temp_{table_name}"
            df[['id', 'detected_topic']].to_sql(
                temp_table, conn, if_exists='replace', index=False)
            
            conn.execute(f"""
                UPDATE {table_name}
                SET detected_topic = (
                    SELECT detected_topic 
                    FROM {temp_table} 
                    WHERE {table_name}.id = {temp_table}.id
                )
                WHERE EXISTS (
                    SELECT 1 
                    FROM {temp_table} 
                    WHERE {table_name}.id = {temp_table}.id
                );
            """)
            conn.execute(f"DROP TABLE {temp_table}")


class TopicAnalyzer:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.preprocessor = TextPreprocessor()
        self.logger = self._setup_logger()
        
        self.topic_model = BERTopic(
            embedding_model=config.embedding_model,
            min_topic_size=config.min_topic_size,
            nr_topics=config.nr_topics,
            hdbscan_model=HDBSCAN(
                min_cluster_size=config.min_cluster_size,
                metric='euclidean',
                cluster_selection_method='eom',
                prediction_data=True
            ),
            representation_model=config.representation_model,
            verbose=config.verbose,
            calculate_probabilities=config.calculate_probabilities
        )
    
    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def analyze(self, texts: Union[List[str], pd.Series]) -> Dict[str, Any]:
        try:
            if isinstance(texts, pd.Series):
                self.logger.info("Processing pandas Series")
                processed_texts = self.preprocessor.process_series(texts)
            else:
                self.logger.info("Processing list of texts")
                processed_texts = self.preprocessor.process_batch(texts)

            self.logger.info("Fitting topic model")
            topics, probs = self.topic_model.fit_transform(processed_texts)
            
            topic_info = self.topic_model.get_topic_info()
            self.logger.info(f"Found {len(topic_info)} topics")
            
            return {
                'topics': topics,
                'probabilities': probs,
                'topic_info': topic_info,
                'topic_model': self.topic_model,
                'processed_texts': processed_texts
            }
            
        except Exception as e:
            self.logger.error(f"Error in topic analysis: {str(e)}")
            raise

    def save_model(self, path: str):
        self.topic_model.save(path)
    
    def load_model(self, path: str):
        self.topic_model = BERTopic.load(path)

def setup_topic_analyzer(model_name: str = "TheBloke/zephyr-7B-alpha-GGUF",
                        prompt_template: str = None) -> TopicAnalyzer:
    if prompt_template is None:
        prompt_template = "<|system|>You are a helpful assistant for labeling topics.</s>\n" \
                         "<|user|>\nTopic documents:\n[DOCUMENTS]\n" \
                         "Keywords: '[KEYWORDS]'\n" \
                         "Create a short topic label.</s><|assistant|>"
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        model_file="zephyr-7b-alpha.Q4_K_M.gguf",
        model_type="mistral",
        gpu_layers=50,
        hf=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-alpha")
    
    generator = pipeline(
        model=model,
        tokenizer=tokenizer,
        task='text-generation',
        max_new_tokens=50,
        repetition_penalty=1.2,
        device=device
    )
    
    representation_model = TextGeneration(generator, prompt=prompt_template)
    
    config = ModelConfig(
        embedding_model='all-mpnet-base-v2',
        min_topic_size=250,
        nr_topics=30,
        min_cluster_size=300,
        representation_model=representation_model
    )
    
    return TopicAnalyzer(config)

topic_analyzer = setup_topic_analyzer()
filename = './data/bigdata.csv'
df = pd.read_csv(filename)
df = df.sample(50000)#, random_state=42)
df = df[~df['comment'].isin(['[deleted]', '[removed]'])]
df = df.reset_index(drop=True)

output = topic_analyzer.analyze(df["comment"])
topics, probs, topic_info, topic_model = output.values