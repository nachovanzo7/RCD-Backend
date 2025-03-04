from rest_framework import serializers
from .models import Capacitacion

class CapacitacionSerializer(serializers.ModelSerializer):
    obra_nombre = serializers.CharField(source="obra.nombre_obra", read_only=True)
    tecnico_nombre = serializers.CharField(source="tecnico.nombre", read_only=True)

    class Meta:
        model = Capacitacion
        fields = ['id', 'fecha', 'motivo', 'obra_nombre', 'tecnico_nombre', 'comentario']
        read_only_fields = ['id']
