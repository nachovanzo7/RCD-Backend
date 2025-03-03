from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from clientes.models import Cliente
from tecnicos.models import Tecnico 
from django.conf import settings


Usuario = get_user_model()

@receiver(post_save, sender=Usuario)
def crear_token_automatico(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        
@receiver(post_migrate)
def create_default_superadmin(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            rol='superadmin'
        )
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_tecnico(sender, instance, created, **kwargs):
    if created and instance.rol == "tecnico":
        Tecnico.objects.create(usuario=instance, nombre=instance.first_name or instance.username)
