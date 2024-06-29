from . import pred
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import * 
from rest_framework import status
from sklearn.preprocessing import FunctionTransformer
import pickle
import numpy as np
import pandas as pd 
# Create your views here.

def predict_crop(input_features):
    nitrogen = float(input_features["Nitrogen"])
    phosphorus = float(input_features["Phosphorus"])
    potassium = float(input_features["Potassium"])
    temperature = np.log(float(input_features["Temperature"]))
    humidity = np.log(float(input_features["Humidity"]))
    PH = float(input_features["pH"])
    rainfall = float(input_features["Rainfall"])
    crop = pred.CropRecommendation(N = nitrogen , Ph = phosphorus,K = potassium,temp = temperature , ph = PH ,humidity= humidity,rainfall=rainfall)
    answer = crop.pred() 
    
    return answer

class Crop (APIView):
    def post (self , request):
        serializer = CropSensorsSerializer(data = request.data)
        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ans = predict_crop(serializer.data)
        return Response(ans, status=status.HTTP_201_CREATED) 