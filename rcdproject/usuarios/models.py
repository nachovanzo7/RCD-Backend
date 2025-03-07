from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    ROLES = [
        ('superadmin', 'Super Administrador'),
        ('coordinador', 'Coordinador de Obra'),
        ('coordinadorlogistico', 'Coordinador Logístico'),
        ('supervisor', 'Supervisor de Obra'),
        ('tecnico', 'Técnico'),
        ('cliente', 'Cliente'),
    ]
    
    rol = models.CharField(
        _('Rol'),
        max_length=21,
        choices=ROLES,
        default='cliente'
    )
    
    email = models.EmailField(
        _('Correo electrónico'),
        unique=True,
        db_index=True
    )
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-date_joined']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permitir que username sea opcional y no único
        self._meta.get_field('username').blank = True
        self._meta.get_field('username')._unique = False

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'rol']

    @property
    def nombre_completo(self):
        # Si en el futuro agregas otro campo para el nombre completo, ajústalo aquí.
        return self.username

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"
