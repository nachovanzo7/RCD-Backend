from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()
from django.contrib.auth.hashers import make_password, check_password


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente', null=True, blank=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=300)
    contacto = models.CharField(max_length=50)
    nombre_contacto = models.CharField(max_length=50)
    fecha_ingreso = models.DateField()
    razon_social = models.CharField(max_length=300)
    direccion_fiscal = models.CharField(max_length=300)
    rut = models.CharField(max_length=300)

    def set_password(self, raw_password):
        self.usuario.password = make_password(raw_password)
        self.usuario.save()
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.usuario.password)
    
    def puede_registrar_mezclado(self):
        ultimo_registro = self.mezclados.order_by('-fecha_registro').first()
        if not ultimo_registro:
            return True
        return (timezone.now() - ultimo_registro.fecha_registro).days >= 30



class SolicitudCliente(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('terminado', 'Terminado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='solicitud', primary_key=True)
