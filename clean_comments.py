import pandas as pd
import re


input_file = r"D:\Jupyter_notebooks\cleaned_twitter_2023.csv"  
output_file = r"D:\Jupyter_notebooks\cleaned_twitter_2023_v1.csv" 


try:
    df = pd.read_csv(input_file, encoding="utf-8")  
    print("Database loaded successfully.")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

def clean_text(text):
    if pd.isnull(text): 
        return text
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'\"#@:/-]', '', text)
    return cleaned_text

if "Post" in df.columns:
    df["Cleaned_Post"] = df["Post"].apply(clean_text)
else:
    print("Error: 'Post' column not found in the database.")
    exit()

try:
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Cleaned database saved to: {output_file}")
except Exception as e:
    print(f"Error saving cleaned file: {e}")
