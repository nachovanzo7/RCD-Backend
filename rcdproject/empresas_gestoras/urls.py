from django.urls import path
from .views import CrearEmpresaGestora, ListarEmpresasGestoras

urlpatterns = [
    path('registro/', CrearEmpresaGestora.as_view(), name='registro-empresa-gestora'),
    path('lista/', ListarEmpresasGestoras.as_view(), name='lista-empresas-gestoras'),
]