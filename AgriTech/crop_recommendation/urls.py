from django.urls import path , include 
from .views import * 
urlpatterns = [
   
    path('predict_crop/', Crop.as_view()),
]
