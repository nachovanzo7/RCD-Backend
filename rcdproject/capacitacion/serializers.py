from rest_framework import serializers
from .models import Capacitacion
from supervisor_obra.serializers import SupervisorObraSerializer  # Importa el serializer corregido

class CapacitacionSerializer(serializers.ModelSerializer):
    obra_nombre = serializers.CharField(source="obra.nombre_obra", read_only=True)
    tecnico_nombre = serializers.CharField(source="tecnico.nombre", read_only=True)
    supervisor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Capacitacion
        fields = [
            'id', 'fecha', 'motivo', 'obra', 'tecnico', 'comentario',
            'obra_nombre', 'tecnico_nombre', 'supervisor', 'supervisor_nombre'
        ]
        extra_kwargs = {
            'supervisor': {'required': False, 'allow_null': True}
        }
        read_only_fields = ['id']

    def get_supervisor_nombre(self, obj):
        if obj.supervisor:
            serializer = SupervisorObraSerializer(obj.supervisor)
            return serializer.data.get('nombre_completo', "No asignado")
        return "No asignado"
