from django.db import models

# Create your models here.
class CropData(models.Model):
    Nitrogen = models.DecimalField(max_digits=5, decimal_places=2)
    Phosphorus = models.DecimalField(max_digits=5, decimal_places=2)
    Potassium = models.DecimalField(max_digits=5, decimal_places=2)
    Temperature = models.DecimalField(max_digits=5, decimal_places=2)
    Humidity = models.DecimalField(max_digits=5, decimal_places=2)
    pH = models.DecimalField(max_digits=4, decimal_places=2)
    Rainfall = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'CropData(N={self.Nitrogen}, P={self.Phosphorus}, K={self.Potassium}, Temp={self.Temperature}, Humidity={self.Humidity}, pH={self.pH}, Rainfall={self.Rainfall})'

