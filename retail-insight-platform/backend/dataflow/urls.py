from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataIngestionLogViewSet, RedisQueueMonitorViewSet

router = DefaultRouter()
router.register(r'logs', DataIngestionLogViewSet)
router.register(r'queue', RedisQueueMonitorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
