from rest_framework import serializers
from .models import Cliente, SolicitudCliente
from obras.models import Obra
from django.contrib.auth import get_user_model
Usuario = get_user_model()

class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra 
        fields = ['id', 'nombre_obra', 'direccion']


class ClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    obras = ObraSerializer(many=True, read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Usuario.objects.all(),
        required=True
    )
    email = serializers.CharField(source="usuario.email", read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id', 'usuario', 'nombre', 'direccion', 'contacto', 'nombre_contacto',
            'fecha_ingreso', 'razon_social', 'direccion_fiscal', 'rut', 'password', 'obras', 'email'
        ]
        read_only_fields = ['id', 'obras', 'email']

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        usuario = validated_data.pop('usuario')
        cliente = Cliente.objects.create(usuario=usuario, **validated_data)
        cliente._raw_password = raw_password
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