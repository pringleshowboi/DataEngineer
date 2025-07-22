from django.shortcuts import render
from rest_framework import viewsets
from .models import SparkJobResult
from .serializers import SparkJobResultSerializer

# Create your views here.
class SparkJobResultViewSet(viewsets.ModelViewSet):
    queryset = SparkJobResult.objects.all().order_by('-run_at')
    serializer_class = SparkJobResultSerializer