import pandas as pd 

df = pd.read_csv("CSV_data/fulldata.csv")

df['time'] = pd.to_datetime(df['time'], errors='coerce')

print(df.info())
print(df.describe())
print(df.duplicated().sum())

print(df.columns)


df['time'] = df['time'].dt.strftime('%Y-%m-%d')
print(df.info())
df.to_json('sm_data.json', orient='records', lines=True)
