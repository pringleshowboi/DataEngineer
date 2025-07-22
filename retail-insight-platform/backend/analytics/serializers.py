from rest_framework import serializers
from .models import SparkJobResult

class SparkJobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparkJobResult
        fields = '__all__'
