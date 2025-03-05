from rest_framework import serializers
from .models import CoordinacionRetiro
from obras.models import Obra
from transportistas.models import Transportista

class CoordinacionRetiroSerializer(serializers.ModelSerializer):
    obra = serializers.PrimaryKeyRelatedField(queryset=Obra.objects.all())
    transportista = serializers.PrimaryKeyRelatedField(queryset=Transportista.objects.all())
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    tecnico_nombre = serializers.CharField(source="tecnico.nombre", read_only=True)
    transportista_nombre = serializers.CharField(source="transportista.nombre", read_only=True)
    empresa_gestora_nombre = serializers.CharField(source="empresa_tratamiento.nombre", read_only=True)

    class Meta:
        model = CoordinacionRetiro
        fields = [
            'id', 'descripcion', 'observaciones', 'estado',
            'fecha_solicitud', 'fecha_retiro', 'pesaje', 'comentarios',
            'tipo_material', 'obra', 'empresa_tratamiento', 'transportista',
            'nombre_obra', 'tecnico_nombre', 'transportista_nombre', 'empresa_gestora_nombre'
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
