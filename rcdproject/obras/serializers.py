from rest_framework import serializers
from .models import Obra, SolicitudObra, Cliente, ArchivoObra

class ArchivoObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoObra
        fields = ['archivo', 'fecha_subida']

class ObraSerializer(serializers.ModelSerializer):
    email_cliente = serializers.CharField(source='cliente.usuario.email', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    tecnico_email = serializers.EmailField(source='tecnico.usuario.email', read_only=True)
    # Se incluye el serializer anidado para listar todos los archivos asociados a la obra
    archivos = ArchivoObraSerializer(many=True, read_only=True)
    
    class Meta:
        model = Obra
        fields = [
            'id',
            'cliente',
            'cliente_nombre',
            'email_cliente',
            'nombre_constructora',
            'nombre_obra',
            'localidad',
            'barrio',
            'direccion',
            'm2_obra',                # Metros cuadrados
            'tipo_construccion',      # Nuevo campo para el tipo de construcción
            'archivos',               # Campo para múltiples archivos
            'cant_pisos',
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
            'cant_visitas_mes',
            'tecnico_email',
        ]
        read_only_fields = ['id']

class SolicitudObraSerializer(serializers.ModelSerializer):
    obra = serializers.IntegerField(source='obra.id', read_only=True)
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    
    class Meta:
        model = SolicitudObra
        fields = ['estado', 'fecha_solicitud', 'obra', 'nombre_obra']
        read_only_fields = ['fecha_solicitud', 'estado', 'obra']

class SolicitudObraAdminSerializer(serializers.ModelSerializer):
    obra = serializers.IntegerField(source='obra.id', read_only=True)
    cliente = serializers.IntegerField(source='obra.cliente.id', read_only=True)
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    
    class Meta:
        model = SolicitudObra
        fields = ['estado', 'fecha_solicitud', 'obra', 'cliente', 'nombre_obra']
        read_only_fields = ['fecha_solicitud', 'obra', 'cliente', 'estado', 'nombre_obra']

from supervisor_obra.models import SupervisorObra

class SupervisorObraSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='usuario.email', read_only=True)
    
    class Meta:
        model = SupervisorObra
        fields = ['id', 'telefono', 'obra', 'nivel_capacitacion', 'email']
