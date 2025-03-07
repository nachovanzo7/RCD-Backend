# serializers.py
from rest_framework import serializers
from .models import EmpresaGestora

class EmpresaGestoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaGestora
        fields = [
            'id',
            'nombre',
            'ubicacion',
            'contacto',
            'email',
            'tipo_material',
        ]
        read_only_fields = ['id']
