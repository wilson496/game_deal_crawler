from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    plain = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=19, decimal_places=2) # Certain bundles on ITAD can reach very high amounts
