from django.urls import path
from .views import (
    ActualizarDatosSuperUsuario, CrearUsuario, LoginView,
    ActualizarUsuario, ListarUsuarios
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('listar/', ListarUsuarios.as_view(), name='listar_usuarios'),
    path('crear/', CrearUsuario.as_view(), name='crear_usuario'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('actualizar-datos-superusuario/', ActualizarDatosSuperUsuario.as_view(), name='actualizar_datos_superusuario'),
    path('editar/<str:email>/', ActualizarUsuario.as_view(), name='editar_usuario_email'),
]
