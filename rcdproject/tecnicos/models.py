from django.db import models

class Tecnico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre", max_length=200)
