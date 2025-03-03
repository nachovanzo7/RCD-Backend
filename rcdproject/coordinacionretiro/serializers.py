from rest_framework import serializers
from .models import CoordinacionRetiro
from obras.models import Obra
from transportistas.models import Transportista

class CoordinacionRetiroSerializer(serializers.ModelSerializer):
    obra = serializers.PrimaryKeyRelatedField(queryset=Obra.objects.all())
    transportista = serializers.PrimaryKeyRelatedField(queryset=Transportista.objects.all())

    class Meta:
        model = CoordinacionRetiro
        fields = [
            'id', 'descripcion', 'observaciones', 'estado',
            'fecha_solicitud', 'fecha_retiro', 'pesaje', 'comentarios',
            'tipo_material', 'obra', 'empresa_tratamiento', 'transportista'
        ]
        read_only_fields = ['id', 'fecha_solicitud']

    def validate(self, data):
        transportista = data.get('transportista')
        tipo_material = data.get('tipo_material')

        if transportista and transportista.estado != 'activo':
            raise serializers.ValidationError("El transportista seleccionado no está activo.")

        if transportista and transportista.tipo_material != tipo_material:
            raise serializers.ValidationError("El transportista seleccionado no puede transportar este tipo de material.")

        return data
