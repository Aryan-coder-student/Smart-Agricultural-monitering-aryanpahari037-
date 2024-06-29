from django.urls import path , include 
from .views import * 
urlpatterns = [
   
    path('predict_irrigation', Irrigation.as_view()),
]
