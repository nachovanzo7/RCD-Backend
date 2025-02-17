from rest_framework import serializers
from .models import Visita

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = ['id', 'obra', 'tecnico','fecha', 'motivo', 'observaciones']
        read_only_fields = ['id']
