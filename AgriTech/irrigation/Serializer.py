from rest_framework import serializers
from .models import *

class IrrigationSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationSensorsModel
        fields = '__all__'
        