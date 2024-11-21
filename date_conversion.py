import pandas as pd

df = pd.read_excel('sentiment_data.xlsx')
df['Time'] = pd.to_datetime(df['Time'], format='%a %b %d %H:%M:%S %z %Y')


print(df['Time'].head())

df['Time'] = df['Time'].dt.tz_localize(None)
print(df['Time'].head())

df['Date'] = df['Time'].dt.date
df['Hour'] = df['Time'].dt.hour
df['Day'] = df['Time'].dt.day_name()
df['Month'] = df['Time'].dt.month_name()


print(df[['Time', 'Date', 'Hour', 'Day', 'Month']].head())
output_file = 'modified_file.xlsx'  
df.to_excel(output_file, index=False)
