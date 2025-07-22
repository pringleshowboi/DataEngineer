import redis
import csv
import json

r = redis.Redis(host='localhost', port=6379, db=0)

with open('Superstore.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r.rpush('order_queue', json.dumps(row))
