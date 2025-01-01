import requests



###### test establishing the ssh connection and data fetching(passed)
"""
import requests

# Endpoint URL
url = "http://127.0.0.1:5000/api/query_posts"

# Headers and JSON payload
headers = {"Content-Type": "application/json"}
data = {
    "platforms": ["twitter"],
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "topic": None,  
    "limit": 10
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print(f"Error making the request: {e}")

"""

##### test fetch reddit api(passed)
"""
url = "http://127.0.0.1:5000/api/reddit_posts"
num_posts:25
headers = {"Content-Type": "application/json"}
data = {
    "url": "https://www.reddit.com/r/test/comments/abcdef/example_post/"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Reddit Test - Status Code:", response.status_code)
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.json())
except Exception as e:
    print(f"Error in fetch_reddit_post: {e}")
"""
