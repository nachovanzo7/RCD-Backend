from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class ActualizarDatosSuperUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, min_length=8)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

Usuario = get_user_model()

class CrearUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'rol')

    def create(self, validated_data):
        # Se usa create_user para que se hashee la contraseña correctamente
        return Usuario.objects.create_user(**validated_data)
