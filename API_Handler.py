import praw
from atproto import Client
import pandas as pd
from googleapiclient.discovery import build
import youtubeAPI
from datetime import datetime, timezone
from tqdm import tqdm

class API_Handler:
    def __init__(self):
        self.reddit_client = praw.Reddit(
            client_id="x4I1ro8_12T669I2lSzNQA",
            client_secret="ZNnBvS10V9Xy0oQT737AG3R0Oe02wA",
            user_agent="Scraper 1.0"
        )
        self.bsky_client = Client()
        self.bsky_client.login('abol3nin7744@gmail.com', 'Ahmed12345')
        self.bsky_client.service = 'https://public.api.bsky.app'

    def fetch_bsky_posts(self, topic, limit=100):
        cursor = None
        params = {
            'q': topic,
            'limit': limit,
            'sort': 'latest',
            'cursor': cursor
        }
        data = self.bsky_client.app.bsky.feed.search_posts(params=params)
        return data.posts

    def fetch_reddit_posts(self, subreddit, num_posts=10):
        # Ensure num_posts doesn't exceed 1000
        num_posts = min(num_posts, 1000)

        # Fetch posts from the subreddit using the "hot" filter
        posts = list(self.reddit_client.subreddit(subreddit).hot(limit=num_posts))
        
        # Create a list to store the submission data
        submissions_data = []

        for post in tqdm(posts):
            post.comments.replace_more(limit=0)  # Remove 'MoreComments' objects
            top_comments = post.comments.list()[:100]  # Get top 100 comments
            
            # Collect data for each comment
            for comment in top_comments:
                comment_timestamp = datetime.fromtimestamp(comment.created_utc, tz=timezone.utc).strftime('%d.%m.%Y')
                submissions_data.append({
                    'username': comment.author.name if comment.author else 'Deleted',
                    'comment': comment.body,
                    'likes': comment.ups,
                    'dislikes': comment.downs,
                    'time': comment_timestamp,
                    'post_title': post.title,
                    'post_url': post.url
                })

        # Convert the collected data into a DataFrame
        df = pd.DataFrame(submissions_data)
        return df.to_dict(orient='records')

handler = API_Handler()

# Example usage for Reddit posts and their comments
#reddit_df = handler.fetch_reddit_posts(subreddit="webscraping", num_posts=10)
#print(reddit_df)

# Example usage for BlueSky posts
#bsky_data = handler.fetch_bsky_posts(query='Health', limit=1)
#for post in bsky_data:
#    print("BlueSky Post:", post.record.text)