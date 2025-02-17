from django.urls import path
from .views import CrearVisita, ListarVisitas

urlpatterns = [
    path('registro/', CrearVisita.as_view(), name='registro-visita'),
    path('lista/', ListarVisitas.as_view(), name='lista-visitas'),
]
