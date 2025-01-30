import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, root_dir)

from API_Handler import API_Handler


@pytest.fixture
def mock_reddit_client():
    mock_client = Mock()
    mock_submission = Mock()
    mock_comment = Mock()

    mock_comment.author = Mock(name='test_user')
    mock_comment.body = 'Test comment'
    mock_comment.ups = 10
    mock_comment.downs = 2
    mock_comment.created_utc = datetime.now(timezone.utc).timestamp()

    mock_submission.title = 'Test Post'
    mock_submission.url = 'https://reddit.com/test'
    mock_submission.comments = Mock()
    mock_submission.comments.list.return_value = [mock_comment]
    mock_submission.comments.replace_more.return_value = None

    mock_subreddit = Mock()
    mock_subreddit.hot.return_value = [mock_submission]
    mock_client.subreddit.return_value = mock_subreddit

    return mock_client


@pytest.fixture
def mock_bsky_client():
    mock_client = Mock()

    mock_app = Mock()
    mock_bsky = Mock()
    mock_feed = Mock()

    mock_feed.search_posts = MagicMock()

    mock_client.app = mock_app
    mock_app.bsky = mock_bsky
    mock_bsky.feed = mock_feed

    mock_post = Mock()
    mock_post.record = Mock(text='Test Bluesky post')
    mock_feed.search_posts.return_value = Mock(posts=[mock_post])

    return mock_client



@pytest.fixture
def api_handler(mock_reddit_client, mock_bsky_client):
    with patch('praw.Reddit', return_value=mock_reddit_client), \
            patch('atproto.Client', return_value=mock_bsky_client):
        handler = API_Handler()
        return handler


def test_init(api_handler):
    assert api_handler.reddit_client is not None
    assert api_handler.bsky_client is not None
    assert api_handler.bsky_client.service == 'https://public.api.bsky.app'


def test_fetch_reddit_posts(api_handler):
    posts = api_handler.fetch_reddit_posts('politics', limit=1)

    assert isinstance(posts, list)
    assert len(posts) > 0

    post = posts[0]
    assert isinstance(post, dict)
    assert all(key in post for key in ['username', 'comment', 'likes', 'dislikes', 'time', 'post_title', 'post_url'])


def test_fetch_reddit_posts_limit(api_handler):
    limit = 5
    posts = api_handler.fetch_reddit_posts('politics', limit=limit)
    assert len(posts) <= limit * 100  # Since each post can have up to 100 comments


def test_fetch_bsky_posts(api_handler):
    posts = api_handler.fetch_bsky_posts('technology', limit=1)

    assert isinstance(posts, list)
    assert len(posts) > 0
    assert hasattr(posts[0], 'record')
    assert hasattr(posts[0].record, 'text')


def test_fetch_bsky_posts_limit(api_handler):
    limit = 5
    posts = api_handler.fetch_bsky_posts('technology', limit=limit)

    assert isinstance(posts, list)
    assert len(posts) > 0


@pytest.mark.parametrize("subreddit,limit", [
    ("python", 10),
    ("news", 5),
    ("technology", 15)
])
def test_fetch_reddit_posts_different_subreddits(api_handler, subreddit, limit):
    posts = api_handler.fetch_reddit_posts(subreddit, limit=limit)
    assert isinstance(posts, list)
    assert len(posts) > 0


def test_error_handling():
    with pytest.raises(Exception):
        handler = API_Handler()
        handler.reddit_client = None
        handler.fetch_reddit_posts('test_subreddit')


def test_reddit_client_error_handling(api_handler):
    api_handler.reddit_client.subreddit.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        api_handler.fetch_reddit_posts('test_subreddit')


def test_bsky_client_error_handling(api_handler):
    api_handler.bsky_client.app.bsky.feed.search_posts = MagicMock(side_effect=Exception("API Error"))
    with pytest.raises(Exception):
        api_handler.fetch_bsky_posts('test_topic')


def test_empty_subreddit(api_handler):
    api_handler.reddit_client.subreddit().hot.return_value = []
    posts = api_handler.fetch_reddit_posts('empty_subreddit')
    assert len(posts) == 0


def test_empty_bsky_search(api_handler):
    api_handler.bsky_client.app.bsky.feed.search_posts = MagicMock(return_value=Mock(posts=[]))
    posts = api_handler.fetch_bsky_posts('nonexistent_topic')
    assert len(posts) == 0