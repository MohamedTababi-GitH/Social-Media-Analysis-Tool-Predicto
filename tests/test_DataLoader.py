import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, root_dir)

from DataLoader import get_ssh_db_connection, query_posts


@pytest.fixture
def mock_engine():
    """Mock SQLAlchemy database engine."""
    mock_engine = MagicMock()
    return mock_engine


@pytest.fixture
def mock_tunnel():
    """Mock SSH tunnel."""
    mock_tunnel = MagicMock()
    return mock_tunnel


@patch("DataLoader.SSHTunnelForwarder")
@patch("DataLoader.create_engine")
def test_get_ssh_db_connection(mock_create_engine, mock_SSHTunnelForwarder, mock_tunnel, mock_engine):
    """Test establishing an SSH tunnel and database connection."""
    mock_SSHTunnelForwarder.return_value = mock_tunnel
    mock_tunnel.local_bind_port = 3306  # Mock SSH Tunnel Port
    mock_create_engine.return_value = mock_engine

    tunnel, engine = get_ssh_db_connection()

    assert tunnel is not None
    assert engine is not None
    mock_SSHTunnelForwarder.assert_called_once()
    mock_create_engine.assert_called_once()


@patch("DataLoader.create_engine")
def test_get_ssh_db_connection_failure(mock_create_engine):
    """Test SSH connection failure."""
    mock_create_engine.side_effect = Exception("Database connection failed")

    tunnel, engine = get_ssh_db_connection()

    assert tunnel is None
    assert engine is None


@patch("DataLoader.query_posts")
def test_query_posts_empty_result(mock_query_posts, mock_engine):
    """Test query_posts when no data is found."""
    mock_query_posts.return_value = pd.DataFrame()  # Return an empty DataFrame

    df = query_posts(mock_engine, platforms=["NonExistentPlatform"])

    assert isinstance(df, pd.DataFrame)
    assert df.empty


@patch("DataLoader.query_posts")
def test_query_posts_with_limit(mock_query_posts, mock_engine):
    """Test query_posts when a limit is applied."""
    mock_query_posts.return_value = pd.DataFrame({
        "PostID": [1, 2, 3],
        "PlatformName": ["Twitter", "Bluesky", "Reddit"]
    })

    df = query_posts(mock_engine, limit=3)

    assert len(df) <= 3
