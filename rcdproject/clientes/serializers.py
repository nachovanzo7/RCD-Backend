from rest_framework import serializers
from .models import Cliente, SolicitudCliente
from obras.models import Obra

class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra 
        fields = ['nombre_obra', 'direccion']


class ClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    obras = ObraSerializer(many=True, read_only=True)  

    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'direccion', 'contacto', 'nombre_contacto',
            'fecha_ingreso', 'razon_social', 'direccion_fiscal', 'rut',
            'mail', 'password', 'obras' 
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        raw_password = validated_data.get('password')
        cliente = Cliente(**validated_data)
        # Guarda la contraseña temporalmente para usarla luego en el signal o en la vista
        cliente._raw_password = raw_password
        cliente.set_password(raw_password)
        cliente.save()
        return cliente

    def create(self, validated_data):
        raw_password = validated_data.get('password')
        cliente = Cliente(**validated_data)
        # Guarda la contraseña temporalmente para usarla luego en el signal o en la vista
        cliente._raw_password = raw_password
        cliente.set_password(raw_password)
        cliente.save()
        return cliente


class SolicitudClienteSerializer(serializers.ModelSerializer):
    cliente_id = serializers.IntegerField(source='cliente.pk', read_only=True)
    
    class Meta:
        model = SolicitudCliente
        fields = ['estado', 'fecha_solicitud', 'cliente_id']
        read_only_fields = ['fecha_solicitud', 'estado']

class SolicitudClienteAdminSerializer(serializers.ModelSerializer):
    cliente_id = serializers.IntegerField(source='cliente.pk', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    
    class Meta:
        model = SolicitudCliente
        fields = ['estado', 'fecha_solicitud', 'cliente_id', 'cliente_nombre']
        read_only_fields = ['fecha_solicitud']
