from rest_framework import serializers
from .models import Visita

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = ['id', 'obra', 'tecnico', 'fecha', 'motivo', 'observaciones']
        read_only_fields = ['id']

    def validate_tecnico(self, value):
        if value is None:
            raise serializers.ValidationError("El campo 'tecnico' es obligatorio.")
        return value
