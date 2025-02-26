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
        # Actualizamos el email si se proporciona
        instance.email = validated_data.get('email', instance.email)
        # Si se proporciona una nueva contraseña, la procesamos con set_password para hashearla
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CrearUsuarioSerializer(serializers.ModelSerializer):
    # La contraseña se recibe en texto plano y se guarda de forma write-only
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Debe tener al menos 8 caracteres."
    )

    class Meta:
        model = Usuario
        # Definimos los campos a trabajar
        fields = ('username', 'email', 'password', 'rol')

    def create(self, validated_data):
        # Se usa el método create_user, que internamente hashea la contraseña
        return Usuario.objects.create_user(**validated_data)
