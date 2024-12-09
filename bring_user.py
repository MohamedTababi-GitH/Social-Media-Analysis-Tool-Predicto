import pandas as pd
import re


input_file = r"D:\Jupyter_notebooks\twitter_2023.csv"  
output_file = r"D:\Jupyter_notebooks\cleaned_twitter_2023.csv" 


try:
    df = pd.read_csv(input_file, encoding="utf-8", low_memory=False) 
    print("Database loaded successfully.")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Function to clean text by removing unknown symbols
def clean_text(text):
    if pd.isnull(text): 
        return text
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'\"#@:/-]', '', text)
    return cleaned_text

# Function to extract the username from the URI column
def extract_username(uri):
    """
    Extract the username from the URI column.
    Example: https://x.com/username/status/... -> username
    """
    if pd.isnull(uri) or not isinstance(uri, str): 
        return None
    match = re.search(r'https://x\.com/([^/]+)/status', uri)
    if match:
        return match.group(1) 
    return None 

# Apply cleaning to the "Post" column or other columns that need cleaning
if "Post" in df.columns:
    df["Cleaned_Post"] = df["Post"].apply(clean_text)
else:
    print("Error: 'Post' column not found in the database.")
    exit()

if "URI" in df.columns:
    df["URI"] = df["URI"].astype(str)
    df["Username"] = df["URI"].apply(extract_username)
else:
    print("Error: 'URI' column not found in the database.")
    exit()

# Save the cleaned data to a new file
try:
    df.to_csv(output_file, index=False, encoding="utf-8")  # Adjust encoding if needed
    print(f"Cleaned database saved to: {output_file}")
except Exception as e:
    print(f"Error saving cleaned file: {e}")
