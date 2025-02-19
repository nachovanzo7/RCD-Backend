from rest_framework import serializers
from .models import Obra, SolicitudObra, Cliente
            

class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = ['id', 'cliente', 'nombre_constructora', 'nombre_obra', 'localidad', 'barrio', 'direccion', 'm2_obra', 'cant_pisos', 'cronograma', 'pedido', 'inicio_obra', 'duracion_obra', 'etapa_obra', 'nombre_jefe_obra', 'telefono_jefe_obra', 'mail_jefe_obra', 'nombre_capataz','telefono_capataz', 'mail_capataz', 'nombre_encargado_supervisor', 'telefono_encargado_supervisor', 'mail_encargado_supervisor', 'cant_visitas_mes', 'imagenes']
        read_only_fields = ['id']

class SolicitudObraSerializer(serializers.ModelSerializer):
    obra = serializers.IntegerField(source='obra.id', read_only=True)
    class Meta:
        model = SolicitudObra
        fields = ['estado', 'fecha_solicitud', 'obra' ]
        read_only_fields = ['fecha_solicitud', 'estado', 'obra' ]

class SolicitudObraAdminSerializer(serializers.ModelSerializer):
    obra = serializers.IntegerField(source='obra.id', read_only=True)
    cliente = serializers.IntegerField(source='obra.cliente.id', read_only=True)
    class Meta:
        model = SolicitudObra
        fields = ['estado', 'fecha_solicitud', 'obra', 'cliente']
        read_only_fields = ['fecha_solicitud', 'obra', 'cliente', 'estado']
