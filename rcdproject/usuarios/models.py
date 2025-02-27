from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    OPCIONES_ROL = [
        ('superadmin', 'Super Administrador'),
        ('coordinador', 'Coordinador de Obra'),
        ('coordinadorlogistico', 'Coordinador Logistico'),
        ('supervisor', 'Supervisor de Obra'),
        ('tecnico', 'Técnico'),
        ('cliente', 'Cliente'),
    ]
    # Los campos username, email y password ya están definidos en AbstractUser
    rol = models.CharField(max_length=50, choices=OPCIONES_ROL)
