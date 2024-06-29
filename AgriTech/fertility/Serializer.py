from rest_framework import serializers
from .models import *

class FertilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilityModel
        fields = '__all__'
        