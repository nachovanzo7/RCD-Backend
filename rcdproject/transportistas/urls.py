from django.urls import path
from .views import CrearTransportista, ListarTransportistas

urlpatterns = [
    path('registro/', CrearTransportista.as_view(), name='registro-transportista'),
    path('lista/', ListarTransportistas.as_view(), name='lista-transportistas'),
]
