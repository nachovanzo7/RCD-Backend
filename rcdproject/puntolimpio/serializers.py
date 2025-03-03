from rest_framework import serializers
from .models import PuntoLimpio
from materiales.serializers import MaterialSerializer
from materiales.models import Material

class PuntoLimpioSerializer(serializers.ModelSerializer):
    materiales = MaterialSerializer(many=True, required=False)
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    
    class Meta:
        model = PuntoLimpio
        fields = [
            'id', 'obra', 'ubicacion', 'accesibilidad', 'metros_cuadrados',
            'estructura', 'tipo_contenedor', 'puntaje', 'señaletica',
            'observaciones', 'clasificacion', 'materiales', 'estado', 'nombre_obra', 'fecha_ingreso'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        materiales_data = validated_data.pop('materiales', [])
        punto = PuntoLimpio.objects.create(**validated_data)
        for material_data in materiales_data:
            cantidad = material_data.pop('cantidad')
            for _ in range(cantidad):
                Material.objects.create(
                    punto_limpio=punto,
                    obra=punto.obra,
                    **material_data
                )
        return punto
