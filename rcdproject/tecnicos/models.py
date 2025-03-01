from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()


class Tecnico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='tecnico', null=True, blank=True)
    nombre = models.CharField(max_length=200)
