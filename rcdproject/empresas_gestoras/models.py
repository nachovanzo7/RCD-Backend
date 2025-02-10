from django.db import models

class EmpresaGestora(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
