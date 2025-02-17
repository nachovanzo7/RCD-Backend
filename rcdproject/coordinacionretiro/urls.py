from django.urls import path
from .views import CrearCoordinacionRetiro, ListarCoordinacionesRetiro, ActualizarEstadoCoordinacionRetiro

urlpatterns = [
    path('registro/', CrearCoordinacionRetiro.as_view(), name='registro-coordinacion'),
    path('lista/', ListarCoordinacionesRetiro.as_view(), name='lista-coordinaciones'),
    path('<int:pk>/actualizarestado/', ActualizarEstadoCoordinacionRetiro.as_view(), name='actualizar-coordinacion'),
]
