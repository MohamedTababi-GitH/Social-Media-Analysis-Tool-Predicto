import pandas as pd
from atproto import Client
from datetime import datetime, timezone , timedelta


# searching for top 100 posts per day in a specific time
def normal_Bsky_Api(query , start_day , start_month , start_year , finish_day , finish_month , finish_year , nb_posts  ) :
    client = Client()
    client.login('abol3nin7744@gmail.com', 'Ahmed12345')
    client.service = 'https://public.api.bsky.app'

    day = start_day
    month = start_month
    year = start_year
    all_posts = []
    cursor = None
    while len(all_posts) < nb_posts:

        try:  # Wrap in a try-except block to catch invalid date errors
            target_day = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc).isoformat()
            end_day = datetime(year, month, day + 1, 0, 0, 0, tzinfo=timezone.utc).isoformat()
        except ValueError:
            # If date is invalid (e.g., Feb 30), move to next month
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
                if year == 2024 and month == 11:
                    break
            continue  # Skip to the next iteration of the loop

        params = {
        'q': query,
        'limit': 100,
        'sort': 'top',
        'since': target_day,
        'until': end_day,
        'cursor': cursor
        }
        day, month , year = increment_date(day, month, year)

        data = client.app.bsky.feed.search_posts(params=params)

        all_posts.extend(data.posts)
        if hasattr(data, 'cursor'):
            cursor = data.cursor
        else:
            break
        if day == finish_day and month == finish_month and year == finish_year:
            break
        # Initialize empty lists to store data
    text_data = []
    created_at_data = []
    author_data = []
    like_count_data = []
    reply_count_data = []
    repost_count_data = []
    uri_of_post = []

    # Extract data from all_posts
    for post in all_posts:
        # Handle any potential missing fields gracefully
        text_data.append(post.record.text if hasattr(post.record, 'text') else "")
        created_at_data.append(post.record.created_at if hasattr(post.record, 'created_at') else None)
        author_data.append(post.author.handle if hasattr(post.author, 'handle') else None)
        like_count_data.append(post.like_count if hasattr(post, 'like_count') else 0)
        reply_count_data.append(post.reply_count if hasattr(post, 'reply_count') else 0)
        repost_count_data.append(post.repost_count if hasattr(post, 'repost_count') else 0)
        uri_of_post.append(post.uri if hasattr(post, 'uri') else None)

    # Create a DataFrame
    data = {
        "Text": text_data,
        "Created At": created_at_data,
        "Author": author_data,
        "Like Count": like_count_data,
        "Reply Count": reply_count_data,
        "Repost Count": repost_count_data,
        "URI": uri_of_post,
    }

    df = pd.DataFrame(data)        

    return  df

#increases day
def increment_date(day, month, year):
    
    # Create a datetime object from the provided day, month, and year
    start_date = datetime(year, month, day)
    
    # Increment the date
    new_date = start_date + timedelta(days=1)
    
    # Extract and return the new day, month, and year
    return new_date.day, new_date.month, new_date.year


# function for searching top comment in a specific time
def Bsky_Api(query , start_day , start_month , start_year , finish_day , finish_month , finish_year , nb_posts  ) :
    client = Client()
    client.login('abol3nin7744@gmail.com', 'Ahmed12345')
    client.service = 'https://public.api.bsky.app'
    
    
    all_posts = []
    cursor = None
    while len(all_posts) < nb_posts:

        try:  # Wrap in a try-except block to catch invalid date errors
            target_day = datetime(start_year, start_month, start_day, 0, 0, 0, tzinfo=timezone.utc).isoformat()
            end_day = datetime(finish_year, finish_month, finish_day, 0, 0, 0, tzinfo=timezone.utc).isoformat()
        except ValueError:
            # If date is invalid (e.g., Feb 30), move to next month
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
                if year == 2024 and month == 11:
                    break
            continue  # Skip to the next iteration of the loop
        params = {
        'q': query,
        'limit': 100,
        'sort': 'top',
        'since': target_day,
        'until': end_day,
        'cursor': cursor
        }
        data = client.app.bsky.feed.search_posts(params=params)
        all_posts.extend(data.posts)
        if hasattr(data, 'cursor'):
            cursor = data.cursor
        else:
            break

        # Initialize empty lists to store data
    text_data = []
    created_at_data = []
    author_data = []
    like_count_data = []
    reply_count_data = []
    repost_count_data = []
    uri_of_post = []

    # Extract data from all_posts
    for post in all_posts:
        # Handle any potential missing fields gracefully
        text_data.append(post.record.text if hasattr(post.record, 'text') else "")
        created_at_data.append(post.record.created_at if hasattr(post.record, 'created_at') else None)
        author_data.append(post.author.handle if hasattr(post.author, 'handle') else None)
        like_count_data.append(post.like_count if hasattr(post, 'like_count') else 0)
        reply_count_data.append(post.reply_count if hasattr(post, 'reply_count') else 0)
        repost_count_data.append(post.repost_count if hasattr(post, 'repost_count') else 0)
        uri_of_post.append(post.uri if hasattr(post, 'uri') else None)

    # Create a DataFrame
    data = {
        "Text": text_data,
        "Created At": created_at_data,
        "Author": author_data,
        "Like Count": like_count_data,
        "Reply Count": reply_count_data,
        "Repost Count": repost_count_data,
        "URI": uri_of_post,
    }

    df = pd.DataFrame(data)        

    return  df

#result =normal_Bsky_Api('health', 4, 12 ,2024,5,12,2024, 20)

#display(result)