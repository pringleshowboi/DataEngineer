from rest_framework import serializers
from .models import DataIngestionLog, RedisQueueMonitor

class DataIngestionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataIngestionLog
        fields = '__all__'

class RedisQueueMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedisQueueMonitor
        fields = '__all__'