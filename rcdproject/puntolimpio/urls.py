from django.urls import path
from .views import CrearPuntoLimpio, ListarPuntosLimpios

urlpatterns = [
    path('registro/', CrearPuntoLimpio.as_view(), name='registro-punto-limpio'),
    path('lista/', ListarPuntosLimpios.as_view(), name='lista-puntos-limpios'),
]

