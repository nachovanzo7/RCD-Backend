from django.urls import path
from .views import CrearFormulario

urlpatterns = [
    path('formularios/crear/', CrearFormulario.as_view(), name='crear_formulario'),
]
