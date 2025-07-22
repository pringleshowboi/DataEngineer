# spark_jobs/process_sales.py
from pyspark.sql import SparkSession
import redis
import json

spark = SparkSession.builder.appName("SalesAnalytics").getOrCreate()

r = redis.Redis(host='redis', port=6379, db=0)
sales = []

while r.llen("sales_queue") > 0:
    data = json.loads(r.lpop("sales_queue"))
    sales.append(data)

df = spark.read.json(spark.sparkContext.parallelize(sales))

# Example transformation
df.groupBy("Region").sum("Sales").show()
