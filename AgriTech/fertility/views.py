from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import * 
from rest_framework import status
import pickle
import numpy as np
import pandas as pd 

"""
N: Nitrogen
P: Phosphorus
K: Potassium
pH: Soil pH (measure of acidity or alkalinity)
EC: Electrical Conductivity (measure of soil salinity)
OC: Organic Carbon
S: Sulfur
Zn: Zinc
Fe: Iron
Cu: Copper
Mn: Manganese
B: Boron
"""

def predict_fertility(input_features):
    with open('fertility/fertility.pkl', 'rb') as file:
        model = pickle.load(file)

    N = float(input_features["N"])
    P = float(input_features["P"])
    K = float(input_features["K"])
    pH = float(input_features["pH"])
    EC = float(input_features["EC"])
    OC = float(input_features["OC"])
    S = float(input_features["S"])
    Zn = float(input_features["Zn"])
    Fe = float(input_features["Fe"])
    Cu = float(input_features["Cu"])
    Mn = float(input_features["Mn"])
    B = float(input_features["B"])

    df_data = {
        "N": [N],
        "P": [P],
        "K": [K],
        "pH": [pH],
        "EC": [EC],
        "OC": [OC],
        "S": [S],
        "Zn": [Zn],
        "Fe": [Fe],
        "Cu": [Cu],
        "Mn": [Mn],
        "B": [B]
    }


    df = pd.DataFrame(df_data)



    return model.predict(df)[0]


class Fertility(APIView):
    def post(self,request):
        serializer = FertilitySerializer(data = request.data)
        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ans = predict_fertility(serializer.data)
        return Response(ans, status=status.HTTP_201_CREATED) 