from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import * 
from rest_framework import status
import pickle
import numpy as np
import pandas as pd 
# Create your views here.



def predict_irrigation(input_features):
    crop_type = input_features["CropType"]
    crop_days = float(input_features["CropDays"])
    soil_moisture = np.sqrt(float(input_features["SoilMoisture"]))
    temperature = np.log1p(float(input_features["Temperature"]))
    humidity = np.log1p(float(input_features["Humidity"]))
        
    df_data = {
            "CropType": [crop_type],
            "CropDays": [crop_days],
            "SoilMoisture": [soil_moisture],
            "temperature": [temperature],
            "Humidity": [humidity]
        }
    df = pd.DataFrame(df_data)
    with open('irrigation/irrigation.pkl', 'rb') as file:
        model = pickle.load(file)
    return model.predict(df)[0]
    
class Irrigation(APIView):
    def post(self, request):
        serializer = IrrigationSensorsSerializer(data = request.data)
        if not serializer.is_valid():
            # serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ans = predict_irrigation(serializer.data)
        return Response(ans, status=status.HTTP_201_CREATED) 
