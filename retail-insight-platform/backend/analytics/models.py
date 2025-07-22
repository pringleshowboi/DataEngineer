from django.db import models
from stores.models import Store
from dataflow.models import IngestionRecord

# Create your models here.
class SparkJobResult(models.Model):
    JOB_CHOICES = [
        ('sales_summary', 'Sales Summary'),
        ('anomaly_detection', 'Anomaly Detection'),
    ]
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=50, choices=JOB_CHOICES)
    run_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    output_summary = models.TextField()

    def __str__(self):
        return f'{self.store.name} - {self.job_type} - {self.run_at}'
    
class AnalyticsResult(models.Model):
    ingestion = models.OneToOneField(IngestionRecord, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    discount = models.FloatField()
    sales = models.FloatField()
    profit = models.FloatField()
    processed_at = models.DateTimeField(auto_now_add=True)

class StoreAnalytics(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    total_sales = models.FloatField(default=0)
    total_orders = models.IntegerField(default=0)
    avg_order_value = models.FloatField(default=0)
    profit_margin = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
