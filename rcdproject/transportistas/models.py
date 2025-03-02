from django.db import models

class Transportista(models.Model):
    TIPOS_MATERIAL_CHOICES = [
        ('escombro_limpio', 'Escombro Limpio'),
        ('plastico', 'Plástico'),
        ('papel_carton', 'Papel y Cartón'),
        ('metales', 'Metales'),
        ('madera', 'Madera'),
        ('mezclados', 'Mezclados'),
        ('peligrosos', 'Peligrosos'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    tipo_vehiculo = models.CharField(max_length=100)
    tipo_material = models.CharField(max_length=20, choices=TIPOS_MATERIAL_CHOICES)

    def __str__(self):
        return self.nombre