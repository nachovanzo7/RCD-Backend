from rest_framework import serializers
from .models import Transportista

class TransportistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportista
        fields = ['id', 'nombre', 'contacto', 'email', 'estado', 'tipo_vehiculo', 'tipo_material']
        read_only_fields = ['id']
