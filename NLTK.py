import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import re
import time

start_time = time.time()


nltk.download('punkt')
nltk.data.path.append(r"D:\Software proj\nltk_data") 
file_path = r"D:\GitHub\Social-Media-Analysis-Tool-Predicto\twitter_2023.csv"
df = pd.read_csv(file_path, dtype=str, low_memory=False)


topics = ["politics", "economics", "food", "entertainment", "travel", "technology"]


def clean_and_tokenize(text):
    if not isinstance(text, str):  
        return []
    text = text.lower()
    text = re.sub(r"http\S+|@\S+|[^a-z\s]", "", text) 
    tokens = word_tokenize(text)
    return [token for token in tokens if token in topics]  


df['Tokens'] = df['Post'].apply(clean_and_tokenize)

all_tokens = [token for tokens in df['Tokens'] for token in tokens]

term_frequency = Counter(all_tokens)

end_time = time.time()


print(f"Processing time (NLTK script): {end_time - start_time:.2f} seconds")
