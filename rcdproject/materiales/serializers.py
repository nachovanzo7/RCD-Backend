from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'punto_limpio', 'transportista', 'descripcion', 'proteccion', 'tipo_contenedor', 'estado_del_contenedor', 'esta_lleno', 'tipo_material', 'ventilacion']
        read_only_fields = ['id']