from rest_framework import serializers
from .models import Obra, SolicitudObra, Cliente

class ObraSerializer(serializers.ModelSerializer):
    # Se obtiene el email del usuario relacionado al cliente
    email_cliente = serializers.CharField(source='cliente.usuario.email', read_only=True)
    
    class Meta:
        model = Obra
        fields = [
            'id',
            'cliente',
            'email_cliente',  # Este campo se usará para filtrar obras según el email
            'nombre_constructora',
            'nombre_obra',
            'localidad',
            'barrio',
            'direccion',
            'm2_obra',
            'cant_pisos',
            'cronograma',
            'pedido',
            'inicio_obra',
            'duracion_obra',
            'etapa_obra',
            'nombre_jefe_obra',
            'telefono_jefe_obra',
            'mail_jefe_obra',
            'nombre_capataz',
            'telefono_capataz',
            'mail_capataz',
            'nombre_encargado_supervisor',
            'telefono_encargado_supervisor',
            'mail_encargado_supervisor',
            'cant_visitas_mes'
        ]
        read_only_fields = ['id']


class SolicitudObraSerializer(serializers.ModelSerializer):
    obra = serializers.IntegerField(source='obra.id', read_only=True)
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    class Meta:
        model = SolicitudObra
        fields = ['estado', 'fecha_solicitud', 'obra', 'nombre_obra']
        read_only_fields = ['fecha_solicitud', 'estado', 'obra' ]

class SolicitudObraAdminSerializer(serializers.ModelSerializer):
    obra = serializers.IntegerField(source='obra.id', read_only=True)
    cliente = serializers.IntegerField(source='obra.cliente.id', read_only=True)
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    
    class Meta:
        model = SolicitudObra
        fields = ['estado', 'fecha_solicitud', 'obra', 'cliente', 'nombre_obra']
        read_only_fields = ['fecha_solicitud', 'obra', 'cliente', 'estado', 'nombre_obra']
