from django.urls import path , include 
from .views import * 
urlpatterns = [
   
    path('predict_fertility/', Fertility.as_view()),
]
