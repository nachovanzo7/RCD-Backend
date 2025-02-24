from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    OPCIONES_ROL = [
        ('super_administrador', 'Super Administrador'),
        ('coordinador_obra', 'Coordinador de Obra'),
        ('cliente', 'Cliente'),
        ('coordinador_retiro', 'Coordinador de Retiro'),
        ('supervisor_obra', 'Supervisor de Obra'),
        ('tecnico', 'Técnico'),
    ]
    # Los campos username, email y password ya están definidos en AbstractUser
    rol = models.CharField(max_length=50, choices=OPCIONES_ROL)
