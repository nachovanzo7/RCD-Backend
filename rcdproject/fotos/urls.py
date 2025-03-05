from django.urls import path
from .views import VerImagenesObra, AgregarImagenesObra

urlpatterns = [
    path('obras/<int:pk>/agregar-imagenes/', AgregarImagenesObra.as_view(), name='agregar-imagenes-obra'),
    path('obras/<int:obra_pk>/imagenes/', VerImagenesObra.as_view(), name='ver-imagenes-obra'),
]
