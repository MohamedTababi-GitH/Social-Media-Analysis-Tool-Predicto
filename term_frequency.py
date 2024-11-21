import pandas as pd
import re
import plotly.express as px


file_path = 'modified_file.xlsx'  
df = pd.read_excel(file_path)


df['Time'] = pd.to_datetime(df['Time'])
df['YearMonth'] = df['Time'].dt.to_period('M')


topics = ["environment", "olimpics", "health", "beauty", "quality", "technology", 
         "price", "cost", "expensive","cheap", "gas", "trump", "kamala", "elections","love","diesel","polution","Joe Biden"]

# Function to clean comments
def clean_comment(text):
    text = str(text).lower() 
    text = re.sub(r"http\S+", "", text) 
    text = re.sub(r"@\S+", "", text)  
    text = re.sub(r"[^a-z\s]", "", text) 
    return text


df['Cleaned_Comment'] = df['Comment'].apply(clean_comment)

trend_data = {topic: [] for topic in topics}
trend_data['Month'] = []  


for period, group in df.groupby('YearMonth'):
    trend_data['Month'].append(str(period))  
    cleaned_comments = group['Cleaned_Comment'].str.cat(sep=' ')  
    for topic in topics:
        trend_data[topic].append(cleaned_comments.count(topic)) 


trend_df = pd.DataFrame(trend_data)

print("Aggregated trends:")
print(trend_df.head())

fig = px.line(
    trend_df,
    x='Month',
    y=[topic for topic in topics],
    title='Custom Topic Trends Over Time',
    labels={'value': 'Frequency', 'variable': 'Topic'},
)
fig.update_layout(xaxis_title='Month', yaxis_title='Frequency of Mentions')
fig.show()
