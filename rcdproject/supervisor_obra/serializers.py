from rest_framework import serializers
from .models import SupervisorObra

class SupervisorObraSerializer(serializers.ModelSerializer):
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    email = serializers.EmailField(source='usuario.email', read_only=True)

    class Meta:
        model = SupervisorObra
        fields = ['id', 'usuario_id', 'nombre_completo', 'telefono', 'obra', 'nivel_capacitacion', 'email']

    def get_nombre_completo(self, obj):
        if obj.usuario and hasattr(obj.usuario, 'nombre_completo'):
            return obj.usuario.nombre_completo
        return "No asignado"
