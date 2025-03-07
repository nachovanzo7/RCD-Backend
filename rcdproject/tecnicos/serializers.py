from rest_framework import serializers
from .models import Tecnico

class TecnicoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="usuario.email", read_only=True)
    class Meta:
        model = Tecnico
        fields = ['id', 'nombre', 'email']
