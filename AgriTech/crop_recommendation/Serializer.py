from rest_framework import serializers
from .models import *

class CropSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropData
        fields = '__all__'
        