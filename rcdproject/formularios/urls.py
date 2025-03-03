from django.urls import path
from .views import CrearFormulario, ListarFormularios

urlpatterns = [
    path('crear/', CrearFormulario.as_view(), name='crear_formulario'),
    path('listar/', ListarFormularios.as_view(), name='list')
]
