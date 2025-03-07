from rest_framework import serializers
from .models import CoordinacionRetiro
from obras.models import Obra
from transportistas.models import Transportista
from empresas_gestoras.models import EmpresaGestora

class CoordinacionRetiroSerializer(serializers.ModelSerializer):
    transportista = serializers.PrimaryKeyRelatedField(
        queryset=Transportista.objects.all(),
        allow_null=True,
        required=False
    )
    empresa_tratamiento = serializers.PrimaryKeyRelatedField(
        queryset=EmpresaGestora.objects.all(),
        allow_null=True,
        required=False
    )
    obra = serializers.PrimaryKeyRelatedField(queryset=Obra.objects.all())

    transportista_nombre = serializers.CharField(source="transportista.nombre", read_only=True)
    empresa_gestora_nombre = serializers.CharField(source="empresa_tratamiento.nombre", read_only=True)

    transportista_contacto = serializers.CharField(source="transportista.contacto", read_only=True)
    empresa_gestora_contacto = serializers.CharField(source="empresa_tratamiento.contacto", read_only=True)

    nombre_obra = serializers.CharField(source="obra.nombre_obra", read_only=True)

    class Meta:
        model = CoordinacionRetiro
        fields = [
            'id',
            'descripcion',
            'observaciones',
            'estado',
            'fecha_solicitud',
            'fecha_retiro',
            'pesaje',
            'comentarios',
            'tipo_material',
            'obra',
            'empresa_tratamiento',
            'transportista',

            'transportista_nombre',
            'empresa_gestora_nombre',

            'transportista_contacto',
            'empresa_gestora_contacto',
            'cantidad',
            'nombre_obra',
        ]
        read_only_fields = ['id', 'fecha_solicitud']
        extra_kwargs = {
            'estado': {'allow_null': True, 'required': False},
            'observaciones': {'allow_null': True, 'required': False},
            'fecha_retiro': {'allow_null': True, 'required': False},
            'pesaje': {'allow_null': True, 'required': False},
        }

    def validate(self, data):
        transportista = data.get('transportista')
        tipo_material = data.get('tipo_material')
        
        if transportista:
            if transportista.estado != 'activo':
                raise serializers.ValidationError(
                    "El transportista seleccionado no está activo."
                )
            if transportista.tipo_material != tipo_material:
                raise serializers.ValidationError(
                    "El transportista seleccionado no puede transportar este tipo de material."
                )

        return data