from django.urls import path
from .views import CrearTecnico, ListarTecnicos

urlpatterns = [
    path('registro/', CrearTecnico.as_view(), name='registro-tecnico'),
    path('lista/', ListarTecnicos.as_view(), name='lista-tecnicos'),
]
