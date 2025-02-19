from django.db import models
from clientes.models import Cliente

class Obra(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='obras')
    nombre_constructora = models.CharField("Nombre de Constructora", max_length=200, null=True, blank=True, default="No especificado")
    nombre_obra = models.CharField("Nombre de Obra", max_length=200, null=True, blank=True, default="No especificado")
    localidad = models.CharField("Localidad", max_length=200, null=True, blank=True, default="No especificado")
    barrio = models.CharField("Barrio", max_length=200, null=True, blank=True, default="No especificado")
    direccion = models.CharField("Dirección", max_length=200, null=True, blank=True, default="No especificado")
    m2_obra = models.DecimalField("M2 Obra", max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    cant_pisos = models.IntegerField("Cantidad de Pisos", null=True, blank=True, default=0)
    cronograma = models.TextField()
    pedido = models.CharField("Pedido", max_length=200, null=True, blank=True, default="No especificado")
    inicio_obra = models.DateField("Inicio de Obra", null=True, blank=True)
    duracion_obra = models.CharField("Duración de Obra", max_length=100, null=True, blank=True, default="No especificado")
    etapa_obra = models.CharField("Etapa de Obra", max_length=100, null=True, blank=True, default="No especificado")
    nombre_jefe_obra = models.CharField("Nombre Jefe de Obra", max_length=200, null=True, blank=True, default="No especificado")
    telefono_jefe_obra = models.CharField("Teléfono Jefe de Obra", max_length=200, null=True, blank=True, default="No especificado")
    mail_jefe_obra = models.CharField("Mail Jefe de Obra", max_length=200, null=True, blank=True, default="No especificado")
    nombre_capataz = models.CharField("Nombre Capataz", max_length=200, null=True, blank=True, default="No especificado")
    telefono_capataz = models.CharField("Teléfono Capataz", max_length=200, null=True, blank=True, default="No especificado")
    mail_capataz = models.CharField("Mail Capataz", max_length=200, null=True, blank=True, default="No especificado")
    nombre_encargado_supervisor = models.CharField("Nombre Encargado de Supervisor Ambiental", max_length=200, null=True, blank=True, default="No especificado")
    telefono_encargado_supervisor = models.CharField("Teléfono del Encargado de Supervisor Ambiental", max_length=200, null=True, blank=True, default="No especificado")
    mail_encargado_supervisor = models.CharField("Mail Encargado de Supervisor Ambiental", max_length=200, null=True, blank=True, default="No especificado")
    cant_visitas_mes = models.IntegerField("Cantidad de Visitas al Mes", null=True, blank=True, default=0)
    imagenes = models.ImageField(upload_to='obras/imagenes/', null=True, blank=True)

class SolicitudObra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    obra = models.OneToOneField(Obra, on_delete=models.CASCADE, related_name='solicitud', primary_key=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
