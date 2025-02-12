from django.urls import path
from .views import CrearMaterial, ListarMateriales

urlpatterns = [
    path('registro/', CrearMaterial.as_view(), name='registro-material'),
    path('lista/', ListarMateriales.as_view(), name='lista-materiales'),
]
