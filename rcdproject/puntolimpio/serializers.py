from rest_framework import serializers
from .models import PuntoLimpio

class PuntoLimpioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoLimpio
        fields = [
           'id', 'obra', 'ubicacion', 'metros_cuadrados',
           'estructura', 'tipo_contenedor', 'puntaje', 'señaletica',
           'observaciones', 'clasificacion'
        ]
        read_only_fields = ['id']
