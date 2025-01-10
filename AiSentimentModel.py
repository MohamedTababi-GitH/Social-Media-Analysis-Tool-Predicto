from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report
import numpy as np
from scipy.special import softmax
import pandas as pd

class SentimentAnalyzer:
    def __init__(self, model_path):
        # load model and tokenizer from path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def preprocess(self, text):
        # Preprocess the text by replacing mentions and URLs
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def predict(self, text):
        # Preprocess and tokenize the input text
        text = self.preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Return the probabilities for negative, neutral, and positive
        return {
            "negative": scores[0],
            "neutral": scores[1],
            "positive": scores[2]
        }

    def analyze_dataframe(self, df, text_column='comment', sentiment_column='sentiment'):
        # Check if the sentiment column exists; if not, add it
        if sentiment_column not in df.columns:
            df[sentiment_column] = None

        # Iterate over the DataFrame and predict sentiment for each row
        for index, row in df.iterrows():
            text = row[text_column]
            probabilities = self.predict(text)
            sentiment = max(probabilities, key=probabilities.get)  # Get the label with the highest probability
            df.at[index, sentiment_column] = sentiment

        return df

# example usage:
#analyzer = SentimentAnalyzer("./checkpoint-900")
#print("result of analysis: ", analyzer.predict("This is a test comment."))

#df = pd.DataFrame({"comment": ["I love this!", "This is terrible.", "Not sure how I feel."]})
#print(df)
#updated_df = analyzer.analyze_dataframe(df)
#print("after df analysis:")
#print(updated_df)
