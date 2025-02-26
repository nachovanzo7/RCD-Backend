from rest_framework import serializers
from .models import Cliente, SolicitudCliente

class ClienteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'direccion', 'contacto', 'nombre_contacto',
            'fecha_ingreso', 'razon_social', 'direccion_fiscal', 'rut',
            'mail', 'password', 'rol'
        ]
        read_only_fields = ['id', 'rol']

    def create(self, validated_data):
        password = validated_data.pop('password')
        cliente = Cliente(**validated_data)
        cliente.set_password(password)
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
