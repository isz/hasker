from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



class Profile(models.Model):
    '''
    Дополнительные поля к пользователю: аватарка, дата регистрации.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_date = models.DateField(verbose_name='Registration date', auto_now_add=True)
    avatar = models.ImageField(verbose_name='Avatar', blank=True, null=True)

    def avatar_url(self):
        try:
            return self.avatar.url
        except:
            return settings.STATIC_URL + '/img/avatar.png'

@receiver(post_save, sender=User)
def create_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()