from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ActualizarDatosSuperUsuario, CrearUsuario, LoginView

urlpatterns = [
    path('actualizar-datos-super-admin/', ActualizarDatosSuperUsuario.as_view(), name='actualizar_datos_superusuario'),
    path('super-admin-crear-usuario/', CrearUsuario.as_view(), name='crear_usuario'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', LoginView.as_view(), name='login'),
]
