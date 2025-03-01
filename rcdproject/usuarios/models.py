from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(AbstractUser):
    OPCIONES_ROL = [
        ('superadmin', 'Super Administrador'),
        ('coordinador', 'Coordinador de Obra'),
        ('coordinadorlogistico', 'Coordinador Logistico'),
        ('supervisor', 'Supervisor de Obra'),
        ('tecnico', 'Técnico'),
        ('cliente', 'Cliente'),
    ]
    rol = models.CharField(max_length=50, choices=OPCIONES_ROL)
    email = models.EmailField(unique=True)  # Se recomienda que el email sea único
