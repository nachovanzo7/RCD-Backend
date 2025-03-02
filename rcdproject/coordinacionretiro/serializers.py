from rest_framework import serializers
from .models import CoordinacionRetiro

class CoordinacionRetiroSerializer(serializers.ModelSerializer):
    obra = serializers.StringRelatedField()
    transportista = serializers.StringRelatedField()
    class Meta:
        model = CoordinacionRetiro
        fields = [
            'id', 'descripcion', 'observaciones', 'estado',
            'fecha_solicitud', 'fecha_retiro', 'pesaje', 'comentarios',
            'tipo_material', 'obra', 'empresa_tratamiento', 'transportista'
        ]
        read_only_fields = ['id', 'fecha_solicitud']

    def validate(self, data):
        """Validar si el transportista puede transportar el material"""
        transportista = data.get('transportista')
        tipo_material = data.get('tipo_material')

        if transportista and transportista.estado != 'activo':
            raise serializers.ValidationError("El transportista seleccionado no está activo.")

        if transportista and transportista.tipo_material != tipo_material:
            raise serializers.ValidationError("El transportista seleccionado no puede transportar este tipo de material.")

        return data




# obra = serializers.StringRelatedField()
#     transportista = serializers.StringRelatedField()