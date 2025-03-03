from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(required=True)

    class Meta:
        model = Material
        fields = [
            'id', 'obra', 'punto_limpio', 'transportista', 'descripcion',
            'proteccion', 'tipo_contenedor', 'estado_del_contenedor',
            'esta_lleno', 'tipo_material', 'ventilacion', 'cantidad'
        ]
        read_only_fields = ['id']
