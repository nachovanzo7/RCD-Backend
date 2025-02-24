from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

Usuario = get_user_model()

@receiver(post_save, sender=Usuario)
def crear_token_automatico(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
