from rest_framework import serializers
from .models import CoordinacionRetiro

class CoordinacionRetiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinacionRetiro
        fields = ['id', 'descripcion', 'observaciones', 'estado', 'fecha_solicitud', 'fecha_retiro', 'pesaje', 'comentarios', 'tipo_material', 'obra', 'empresa_tratamiento', 'transportista']
        read_only_fields = ['id', 'fecha_solicitud']
