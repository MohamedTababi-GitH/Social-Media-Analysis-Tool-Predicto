import pandas as pd
from transformers import pipeline
import plotly.express as px

# to be linked directly with our database
# with distilbert we have no neutrals, only positives and negatives
file_path = 'sentiment_data.xlsx'  
df = pd.read_excel(file_path)

df['Comment'] = df['Comment'].fillna('') 

if 'Sentiment' not in df.columns:
    df['Sentiment'] = ''

sentiment_analyzer = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")

for index, row in df.iterrows():
    text = row['Comment']
    if text.strip(): 
        result = sentiment_analyzer(text)
        sentiment = result[0]['label']  
        df.at[index, 'Sentiment'] = sentiment
        print(f"Text: {text}\nSentiment: {sentiment}\n")  
        df.at[index, 'Sentiment'] = sentiment

sentiment_counts = df['Sentiment'].value_counts()

chart_data = pd.DataFrame({
    'Sentiment': sentiment_counts.index,
    'Count': sentiment_counts.values
})


fig = px.pie(chart_data, values='Count', names='Sentiment', title='Sentiment Distribution')
fig.show()
