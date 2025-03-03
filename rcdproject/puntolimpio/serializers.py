from rest_framework import serializers
from .models import PuntoLimpio
from materiales.serializers import MaterialSerializer
from materiales.models import Material

class PuntoLimpioSerializer(serializers.ModelSerializer):
    # Eliminamos write_only para que se liste también en las respuestas GET
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
        # Extraer datos de materiales (si se proporcionan)
        materiales_data = validated_data.pop('materiales', [])
        # Crear el punto limpio
        punto = PuntoLimpio.objects.create(**validated_data)
        # Por cada material, crea la cantidad indicada
        for material_data in materiales_data:
            cantidad = material_data.pop('cantidad')
            for _ in range(cantidad):
                # Se asigna automáticamente el punto limpio y se usa la obra del mismo
                Material.objects.create(
                    punto_limpio=punto,
                    obra=punto.obra,
                    **material_data
                )
        return punto
