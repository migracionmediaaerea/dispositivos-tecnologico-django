from catalogos_modular.models import Token, User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def delete_tokens(sender, instance, **kwargs):
    new_password = instance.password
    try:
        old_password = User.objects.get(id=instance.id).password
    except User.DoesNotExist:
        old_password = None
    if new_password != old_password:
        # Get tokens
        Token.objects.filter(user=instance).delete()