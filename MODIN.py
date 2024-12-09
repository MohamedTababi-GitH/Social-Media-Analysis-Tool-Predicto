import pandas as pd
import time
import re


start_time = time.time()


file_path = r"D:\GitHub\Social-Media-Analysis-Tool-Predicto\twitter_2023.csv"
df = pd.read_csv(file_path, dtype=str, low_memory=False)  # Read CSV directly

# Clean comments
def clean_comment(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    return text


topics = [
    "politics", "economics", "food", "entertainment", "travel", "technology"
]

# Clean comments column
df['Cleaned_Comment'] = df['Post'].apply(clean_comment)


df['Date'] = pd.to_datetime(df['Time'], errors='coerce')
df = df.dropna(subset=['Date'])
df['YearMonth'] = df['Date'].dt.to_period('M')

# Calculate total occurrences by month
monthly_counts = []
for period, group in df.groupby('YearMonth'):
    cleaned_comments = " ".join(group['Cleaned_Comment'].tolist())
    counts = {topic: cleaned_comments.count(topic) for topic in topics}
    counts['Month'] = str(period)
    monthly_counts.append(counts)


monthly_counts_df = pd.DataFrame(monthly_counts)

# Calculate total occurrences for each topic
cleaned_comments = " ".join(df['Cleaned_Comment'].tolist())
total_counts = {topic: cleaned_comments.count(topic) for topic in topics}


total_counts_df = pd.DataFrame(total_counts.items(), columns=['Topic', 'Total Occurrences'])

end_time = time.time()

print(f"Processing time (Modin script): {end_time - start_time:.2f} seconds")
