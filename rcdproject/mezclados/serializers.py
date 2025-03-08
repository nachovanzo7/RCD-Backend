from rest_framework import serializers
from .models import Mezclado, MezcladoImagen

class ImagenMezcladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MezcladoImagen
        fields = ['id', 'imagen', 'fecha_subida']
        read_only_fields = ['id', 'fecha_subida']

class MezcladoSerializer(serializers.ModelSerializer):
    # Se muestra el nombre de la obra asociada
    nombre_obra = serializers.CharField(source='obra.nombre_obra', read_only=True)
    # Se incluyen las imágenes asociadas
    imagenes = ImagenMezcladoSerializer(many=True, read_only=True)

    class Meta:
        model = Mezclado
        fields = ['id', 'obra', 'nombre_obra', 'pesaje', 'fecha_registro', 'imagenes']
        read_only_fields = ['id', 'fecha_registro']

    def create(self, validated_data):
        # Para manejar múltiples imágenes, se espera que en la request se envíen archivos en la clave 'imagenes'
        request = self.context.get('request')
        imagenes_data = request.FILES.getlist('imagenes') if request else []

        mezclado = Mezclado.objects.create(**validated_data)
        for imagen in imagenes_data:
            MezcladoImagen.objects.create(mezclado=mezclado, imagen=imagen)
        return mezclado
