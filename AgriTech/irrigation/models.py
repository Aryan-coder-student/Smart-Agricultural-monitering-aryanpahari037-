from django.db import models

# Create your models here.
class IrrigationSensorsModel(models.Model):
    
    CropType =models.IntegerField()
    CropDays = models.IntegerField()
    SoilMoisture = models.DecimalField(max_digits=6, decimal_places=2)
    Temperature = models.DecimalField(max_digits=6, decimal_places=2)
    Humidity = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.CropType