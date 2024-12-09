import pandas as pd
import os

def split_csv(input_file, output_dir, chunk_size):
    """
    Splits a large CSV file into smaller CSV files.

    """

    os.makedirs(output_dir, exist_ok=True)


    try:
        for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size, encoding="utf-8")):
            output_file = os.path.join(output_dir, f"split_{i + 1}.csv")
            chunk.to_csv(output_file, index=False, encoding="utf-8")
            print(f"Created: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Usage
input_file = "D:\Jupyter_notebooks\cleaned_twitter_2023_v1.csv" 
output_dir = "D:\Jupyter_notebooks\split_data"
chunk_size = 10000 

split_csv(input_file, output_dir, chunk_size)
