from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    OPCIONES_ROL = [
        ('super_administrador', 'Super Administrador'),
        ('coordinador_obra', 'Coordinador de Obra'),
        ('coordinador_logistico', 'Coordinador Logistico'),
        ('supervisor_obra', 'Supervisor de Obra'),
        ('tecnico', 'Técnico'),
        ('cliente', 'Cliente'),
    ]
    # Los campos username, email y password ya están definidos en AbstractUser
    rol = models.CharField(max_length=50, choices=OPCIONES_ROL)
