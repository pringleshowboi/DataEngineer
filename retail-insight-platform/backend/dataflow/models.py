from django.db import models
from stores.models import Store

# Create your models here.
class DataIngestionLog(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.store.name} - {self.status} at {self.timestamp}'

class RedisQueueMonitor(models.Model):
    queue_name = models.CharField(max_length=100)
    current_size = models.IntegerField()
    checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.queue_name} - {self.current_size} items'
    
class IngestionRecord(models.Model):
    order_id = models.CharField(max_length=50)
    order_date = models.DateField()
    ship_date = models.DateField()
    customer_name = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('queued', 'Queued'), ('processed', 'Processed')])
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    order_date = models.DateField()
    ship_date = models.DateField()
    customer_name = models.CharField(max_length=200)
    segment = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    sales = models.FloatField()
    quantity = models.IntegerField()
    profit = models.FloatField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)  # e.g., 'pending', 'running', 'success', 'failed'
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  # in seconds
    logs = models.TextField(blank=True)  # optional logs or error messages

    def __str__(self):
        return f"Job {self.job_id} ({self.status})"