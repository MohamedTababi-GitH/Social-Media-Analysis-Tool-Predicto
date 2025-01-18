import modin.pandas as pd
from newsapi import NewsApiClient
import re
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
import nltk
from DataLoader import * 
from DataPreprocessor import inspect_data
from TrendAnalyzer import *


def analyze_frequency_modin(data,topics = None, start_date=None,end_date=None):

    if topics is None:
    
        topics = ["politics", "economics", "food", "entertainment", "travel", "technology"]

    data['Date'] = pd.to_datetime(data['Timestamp'], errors='coerce')
    data = data.dropna(subset=['Date'])

    if start_date:
        data = data[data['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data['Date'] <= pd.to_datetime(end_date)]

    # group by month
    data['YearMonth'] = data['Date'].dt.to_period('M')
    monthly_counts = []

    for period, group in data.groupby('YearMonth'):
        combined_comments = " ".join(group['PostContent'].tolist())
        counts = {topic: combined_comments.count(topic) for topic in topics}
        counts['Month'] = str(period)
        monthly_counts.append(counts)
        
    monthly_counts_df = pd.DataFrame(monthly_counts)

    # total topic counts
    combined_comments = " ".join(data['PostContent'].tolist())
    total_counts = {topic: combined_comments.count(topic) for topic in topics}
    total_counts_df = pd.DataFrame(total_counts.items(), columns=['Topic','Total Occurences'])

    return monthly_counts_df, total_counts_df

def get_top_topics(data, column="PostContent", start_date=None, end_date=None, top_n=10):
    if "Timestamp" in data:
        data["Timestamp"] = pd.to_datetime(data["Timestamp"], errors="coerce")

    if start_date:
        data = data[data["Timestamp"] >= pd.to_datetime(start_date)]
    if end_date:
        data = data[data["Timestamp"] <= pd.to_datetime(end_date)]

    combined_text = " ".join(data[column].dropna().tolist())
    combined_text = re.sub(r"http\S+|www\S+", "", combined_text)  # Remove URLs

    words = re.findall(r'\b\w+\b', combined_text.lower())
    try:
        stop_words = set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords")
        stop_words = set(stopwords.words("english"))
    custom_stop_words = {
    "like", "https", "chat", "new", "amp", "use", "chatgpt", "gpt", "using", 
    "one", "would", "also", "could", "many", "much", "get", "even", "still", 
    "make", "really", "know", "think", "want", "need", "good", "great", 
    "best", "better", "bad", "well", "look", "see", "yes", "no", "way", 
    "time", "day", "year", "people", "thing", "stuff", "lot", "always", 
    "never", "ever", "now", "just", "more", "less", "first", "last", "next", 
    "back", "around", "every", "another", "someone", "something", "everyone", 
    "everything", "nothing", "some", "any", "really", "about", "what", 
    "when", "where", "why", "how", "which", "this", "that", "these", "those",
    "here", "there", "each", "few", "such", "thus", "therefore", "hence",
    "meanwhile", "besides", "though", "although", "maybe", "perhaps", 
    "however", "already", "still", "almost", "actually", "indeed", "either", 
    "neither", "likely", "probably", "certainly", "sure", "always", 
    "sometimes", "often", "never", "yet", "though", "through", "across", 
    "between", "while", "with", "without", "within", "among", "amongst", 
    "towards", "against", "upon", "onto", "under", "over", "below", "above",
    "into", "out", "inside", "outside", "via", "whether", "either", "neither"
    }

    stop_words.update(custom_stop_words)

    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    word_counts = Counter(filtered_words)
    top_topics = word_counts.most_common(top_n)
    return pd.DataFrame(top_topics, columns=["Topic", "Frequency"])


def recommend_news_from_api(topics_df, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    recommendations = []
    
    for _, row in topics_df.iterrows():
        topic = row["Topic"]

        # Fetch relevant news articles
        articles = newsapi.get_everything(
            q=topic,
            sources='bbc-news',
            domains='bbc.co.uk,techcrunch.com',
            language="en",
            sort_by="relevancy",
            from_param="2024-12-18",  # Adjusted start date
            to="2025-01-16",
            page_size=10
        )

        # Extract article URLs if available
        urls = [article["url"] for article in articles.get("articles", []) if "url" in article]
        
        if urls:
            recommendations.append((topic, urls[:5]))  # Return only top 5

    return recommendations

#tunnel, engine = get_ssh_db_connection()
#parameters
"""
platforms
start_date
end_date
get_top_topics
"""
#df = query_posts(
 #               engine,
  #              platforms=["bluesky", "twitter"],
   #             start_date="2023-01-01",
    #            end_date="2023-12-31",
     #           topic="food",
      #          limit=500
       #         )


#inspect_data(df)
#monthly, total = analyze_frequency_modin(df, "food","2023-01-01","2023-12-31" )
#print(df.columns)
#display(monthly)
#display(total)



#newdf = pd.read_csv("CSV_data/fulldata.csv")
#print(newdf.columns)
