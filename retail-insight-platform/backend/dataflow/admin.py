from django.contrib import admin
from .models import DataIngestionLog, RedisQueueMonitor
# Register your models here.
admin.site.register(DataIngestionLog)
admin.site.register(RedisQueueMonitor)
