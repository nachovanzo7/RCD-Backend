from django.urls import path
from .views import CrearFormulario, ListarFormularios, DetalleFormulario

urlpatterns = [
    path('crear/', CrearFormulario.as_view(), name='crear_formulario'),
    path('listar/', ListarFormularios.as_view(), name='list'),
    path('detalle/<int:pk>/', DetalleFormulario.as_view(), name='detalle-formulario'),
]
