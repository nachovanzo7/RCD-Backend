from rest_framework import serializers
from .models import Tecnico

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['id', 'nombre']
        read_only_fields = ['id']

