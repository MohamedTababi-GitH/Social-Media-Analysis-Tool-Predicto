Overview
This project includes two scripts to analyze and visualize text data:

Sentiment Analysis: Classifies comments as positive or negative and shows results as a pie chart.
Topic Trends: Tracks the frequency of predefined topics over time and visualizes them in a line chart.

Script 1: Sentiment Analysis

What it does: Uses a DistilBERT model to analyze sentiments in user comments.
Input file: your_data.xlsx (requires Comment column).
Output: A pie chart showing positive vs. negative sentiment distribution.

How to use:
Place sentiment_data.xlsx in the same folder as the script.
Run the script to see the sentiment results and chart.

Script 2: Topic Trends

What it does: Tracks topics (e.g., environment, technology, elections) mentioned in comments over time.
Input file: your_file.xlsx (requires Time and Comment columns).
Output: A line chart showing topic trends by month.

How to use:
Place your_file.xlsx in the same folder as the script.
Run the script to generate the topic trend chart.

Before running the script please install the following:

pip install pandas transformers plotly




