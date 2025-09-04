from django.shortcuts import render
from rest_framework import viewsets
from .models import DataIngestionLog, RedisQueueMonitor
from .serializers import DataIngestionLogSerializer, RedisQueueMonitorSerializer

# Create your views here.
class DataIngestionLogViewSet(viewsets.ModelViewSet):
    queryset = DataIngestionLog.objects.all().order_by('-timestamp')
    serializer_class = DataIngestionLogSerializer

class RedisQueueMonitorViewSet(viewsets.ModelViewSet):
    queryset = RedisQueueMonitor.objects.all().order_by('-checked_at')
    serializer_class = RedisQueueMonitorSerializer