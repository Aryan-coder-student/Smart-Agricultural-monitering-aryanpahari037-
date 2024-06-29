from django.db import models

# Create your models here.
class FertilityModel(models.Model):
    N = models.DecimalField(max_digits=5, decimal_places=2)
    P = models.DecimalField(max_digits=5, decimal_places=2)
    K = models.DecimalField(max_digits=5, decimal_places=2)
    pH = models.DecimalField(max_digits=4, decimal_places=2)
    EC = models.DecimalField(max_digits=5, decimal_places=2)
    OC = models.DecimalField(max_digits=5, decimal_places=2)
    S = models.DecimalField(max_digits=5, decimal_places=2)
    Zn = models.DecimalField(max_digits=5, decimal_places=2)
    Fe = models.DecimalField(max_digits=5, decimal_places=2)
    Cu = models.DecimalField(max_digits=5, decimal_places=2)
    Mn = models.DecimalField(max_digits=5, decimal_places=2)
    B = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.pH