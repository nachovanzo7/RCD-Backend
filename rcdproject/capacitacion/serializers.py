from rest_framework import serializers
from .models import Capacitacion

class CapacitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacitacion
        fields = ['id', 'fecha', 'motivo', 'obra', 'tecnico', 'comentario']
        read_only_fields = ['id']
