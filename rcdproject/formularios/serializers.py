from rest_framework import serializers
from .models import Formularios

class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formularios
        fields = '__all__'
