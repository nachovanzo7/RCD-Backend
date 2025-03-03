from rest_framework import serializers
from .models import Formularios

class FormularioSerializer(serializers.ModelSerializer):
    tecnico_nombre = serializers.CharField(source='tecnico.nombre', read_only=True)
    obra_nombre = serializers.CharField(source='obra.nombre_obra', read_only=True)

    class Meta:
        model = Formularios
        fields = '__all__'
