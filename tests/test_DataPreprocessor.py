import pytest
import pandas as pd
import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, root_dir)

from DataPreprocessor import datapreprocessor

# Sample test DataFrame
@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'comment': [
            "Hello World!",  # Simple text
            "   Extra Spaces   ",  # Leading & trailing spaces
            "Hello World!",  # Duplicate
            "https://example.com",  # URL
            "Text with 😊 emoji",  # Emoji
            "Text!! With??? Punctuation!!!",  # Punctuation
            "",  # Empty string
            None  # NaN value
        ]
    })
    return data


def test_missing_comment_column():
    """Test that function raises an error if 'comment' column is missing."""
    df = pd.DataFrame({'other_column': ["Hello", "World"]})
    with pytest.raises(ValueError, match="The DataFrame must contain a column named 'comment'"):
        datapreprocessor(df)


def test_remove_empty_comments(sample_data):
    """Test that NaN and empty comments are removed."""
    processed_df = datapreprocessor(sample_data)
    assert "" not in processed_df['comment'].values
    assert processed_df['comment'].isna().sum() == 0


def test_remove_urls(sample_data):
    """Test that URLs are removed from comments."""
    processed_df = datapreprocessor(sample_data)
    assert not any("http" in comment for comment in processed_df['comment'])


def test_remove_duplicates(sample_data):
    """Test that duplicate comments are removed."""
    processed_df = datapreprocessor(sample_data)
    assert processed_df.duplicated(subset='comment').sum() == 0


def test_lowercase_conversion(sample_data):
    """Test that all comments are converted to lowercase."""
    processed_df = datapreprocessor(sample_data)
    assert all(comment == comment.lower() for comment in processed_df['comment'])


def test_whitespace_normalization(sample_data):
    """Test that extra spaces within comments are removed."""
    processed_df = datapreprocessor(sample_data)
    assert all("  " not in comment for comment in processed_df['comment'])


def test_punctuation_removal(sample_data):
    """Test that non-alphanumeric characters (punctuation) are removed."""
    processed_df = datapreprocessor(sample_data)
    assert all(comment.isalnum() or " " in comment for comment in processed_df['comment'])


def test_emoji_conversion(sample_data):
    """Test that emojis are converted to text representation."""
    processed_df = datapreprocessor(sample_data)
    assert "😊" not in processed_df['comment'].values  # No raw emojis
    assert any("smiling_face_with_smiling_eyes" in comment for comment in processed_df['comment'])


def test_index_reset(sample_data):
    """Ensure that the DataFrame index is reset after processing."""
    processed_df = datapreprocessor(sample_data)
    assert (processed_df.index == range(len(processed_df))).all()


if __name__ == "__main__":
    pytest.main()
