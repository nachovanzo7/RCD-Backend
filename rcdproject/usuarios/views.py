from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import ActualizarDatosSuperUsuarioSerializer, CrearUsuarioSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.permissions import IsAuthenticated
from .permisos import RutaProtegida

Usuario = get_user_model()

class ActualizarDatosSuperUsuario(APIView):
    """
    Vista que permite al superusuario modificar su email y contraseña.
    Se requiere autenticación.
    """
    permission_classes = [IsAuthenticated] 
     # Asegúrate de que el usuario esté autenticado

    def put(self, request):
        # Suponemos que el usuario autenticado es el que se desea modificar.
        usuario = request.user

        # Verificamos que el usuario tenga el rol de superadministrador (opcional)
        if usuario.rol != 'super_administrador':
            return Response({"error": "No tienes permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ActualizarDatosSuperUsuarioSerializer(instance=usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Datos actualizados correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

Usuario = get_user_model()

class CrearUsuario(APIView):
    """
    Vista que permite al superadministrador crear nuevos usuarios con un rol específico.
    """
    permission_classes = [RutaProtegida(['super_administrador'])]

    def post(self, request):
        serializer = CrearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                usuario = serializer.save()
            except DjangoValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "mensaje": "Usuario creado exitosamente.",
                "usuario": {
                    "username": usuario.username,
                    "email": usuario.email,
                    "rol": usuario.rol
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
