from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode, lower, split
from pyspark.sql.types import ArrayType, StringType
import time

start_time = time.time()


# Initialize Spark session 
spark = (SparkSession.builder
    .appName("SocialMediaAnalysis")
    .master("local[*]")       
    .getOrCreate())

# Suppress verbose logs
spark.sparkContext.setLogLevel("ERROR")

file_path = r"D:\GitHub\Social-Media-Analysis-Tool-Predicto\twitter_2023.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Define the list of specific topics
words_to_count = {"politics", "economics", "food", "entertainment", "travel", "technology"}

word_count_df = (df.withColumn("word", explode(split(lower(col("Post")), r"[^\w]+")))  
                   .filter(col("word").isin(words_to_count))  
                   .groupBy("word")  
                   .count() 
                   .orderBy("count", ascending=False)) 

word_count_df.show()

end_time = time.time()

print(f"Processing time (Spark script): {end_time - start_time:.2f} seconds")

spark.stop()
