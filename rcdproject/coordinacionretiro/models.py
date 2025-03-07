from django.db import models
from obras.models import Obra
from empresas_gestoras.models import EmpresaGestora  
from transportistas.models import Transportista
from materiales.models import Material

class CoordinacionRetiro(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('inactivo', 'Inactivo'),
    ]

    descripcion = models.TextField("Descripción")
    observaciones = models.TextField("Observaciones", blank=True, null=True)
    
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',  
        blank=True,
        null=True
    )

    fecha_solicitud = models.DateTimeField("Fecha de Solicitud", auto_now_add=True)
    
    fecha_retiro = models.DateTimeField(
        "Fecha de Retiro", 
        blank=True, 
        null=True
    )
    pesaje = models.DecimalField(
        "Pesaje", 
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    
    cantidad = models.DecimalField(
        "Cantidad", 
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    
    comentarios = models.TextField(
        "Comentarios", 
        blank=True, 
        null=True
    )

    tipo_material = models.CharField(
        "Tipo de Material",
        max_length=20,
        choices=Material.TIPO_MATERIAL_CHOICES
    )

    obra = models.ForeignKey(
        Obra,
        on_delete=models.CASCADE,
        related_name='coordinaciones_retiro',
        verbose_name="Obra"
    )

    empresa_tratamiento = models.ForeignKey(
        EmpresaGestora,
        on_delete=models.SET_NULL,
        related_name='coordinaciones_retiro',
        verbose_name="Empresa de Tratamiento",
        blank=True,
        null=True
    )

    transportista = models.ForeignKey(
        Transportista,
        on_delete=models.SET_NULL,
        related_name='coordinaciones_retiro',
        verbose_name="Transportista",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Coordinación ({self.pk}) - {self.descripcion}"
