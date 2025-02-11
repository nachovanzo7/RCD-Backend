from django.urls import path
from .views import CrearEmpresaGestora, ListarEmpresasGestoras, ModificarDatosEmpresaGestora, EliminarEmpresaGestora


urlpatterns = [
    path('registro/', CrearEmpresaGestora.as_view(), name='registro-empresa-gestora'),
    path('lista/', ListarEmpresasGestoras.as_view(), name='lista-empresas-gestoras'),
    path('modificar/<int:pk>/', ModificarDatosEmpresaGestora.as_view(), name='modificar-empresa-gestora'),
    path('eliminar/<int:pk>/', EliminarEmpresaGestora.as_view(), name='eliminar-empresa-gestora'),
]
