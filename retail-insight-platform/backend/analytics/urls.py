from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SparkJobResultViewSet

router = DefaultRouter()
router.register(r'jobs', SparkJobResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]