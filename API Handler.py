import praw
from atproto import Client
import pandas as pd
from googleapiclient.discovery import build
import youtubeAPI

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


    def fetch_bsky_posts(self, query, limit=100):
        cursor=None
        params = {
            'q': query,
            'limit': limit,
            'sort': 'latest',
            'cursor': cursor
        }
        data = self.bsky_client.app.bsky.feed.search_posts(params=params)
        return data.posts

    def fetch_reddit_post(self, url):
        return self.reddit_client.submission(url=url)



handler = API_Handler()

reddit_post = handler.fetch_reddit_post(url="https://www.reddit.com/r/webscraping/comments/19bekjv/is_there_a_current_solution_to_scrap_tweets/")
print("Reddit Post:", reddit_post.selftext)


bsky_data = handler.fetch_bsky_posts(query='Health', limit=1)
for post in bsky_data:
    print("BlueSky Post:", post.record.text)
