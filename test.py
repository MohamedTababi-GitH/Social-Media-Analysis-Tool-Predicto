import requests



###### test establishing the ssh connection and data fetching(passed)


"""
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
limit:25
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


##### test fetch bluesky api(all good)
"""
url = "http://127.0.0.1:5000/api/bsky_posts"
headers = {"Content-Type": "application/json"}
data = {
    "topic": "test", 
    "limit": 5       
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("BlueSky Test - Status Code:", response.status_code)
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.json())
except Exception as e:
    print("error")
"""

##### test fetch youtube api(all good)
"""
url = "http://127.0.0.1:5000/api/youtube_comments"
headers = {"Content-Type": "application/json"}
data = {
    "topic": "Example Topic", 
    "start_date": "2023-01-01T00:00:00",  
    "end_date": "2023-12-31T23:59:59",    
    "limit": 5  # Optional, default is 100 if not specified     
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("BlueSky Test - Status Code:", response.status_code)
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.json())
except Exception as e:
    print("error")
"""

