from django.urls import path
from .views import lista_notificaciones

urlpatterns = [
    path('cliente/<int:cliente_id>/', lista_notificaciones, name='lista_notificaciones'),
]
