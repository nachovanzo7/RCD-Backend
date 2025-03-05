from django.urls import path
from .views import CrearTransportista, ListarTransportistas, ModificarDatosTransportista, EliminarTransportista, DetalleTransportista, ActualizarTransportista


urlpatterns = [
    path('registro/', CrearTransportista.as_view(), name='registro-transportista'),
    path('lista/', ListarTransportistas.as_view(), name='lista-transportistas'),
    path('modificar/<int:pk>/', ModificarDatosTransportista.as_view(), name='modificar-transportista'),
    path('eliminar/<int:pk>/', EliminarTransportista.as_view(), name='eliminar-transportista'),
    path('<int:pk>/', DetalleTransportista.as_view(), name='detalle-transportista'),
    path('<int:pk>/actualizar/', ActualizarTransportista.as_view(), name='actualizar-transportista'),

]

