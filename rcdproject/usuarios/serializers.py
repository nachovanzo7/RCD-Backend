from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class ActualizarDatosSuperUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        help_text="Debe tener al menos 8 caracteres."
    )

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CrearUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('email', 'password', 'rol', 'username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),  # Auto username
            password=validated_data['password'],
            rol=validated_data['rol']
        )
        return user
    
from obras.models import Obra
class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.ChoiceField(choices=Usuario.ROLES)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
