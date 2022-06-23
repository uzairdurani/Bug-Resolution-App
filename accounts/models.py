from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.http.request import validate_host
import os
from django.conf import settings
# Create your models here.


def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, default='user/avatar.jpg')
    bio = models.TextField(max_length=500, blank=True)

    def clean(self) -> None:
        if not self.avatar:
            raise ValidationError('x')
        else:
            w, h = get_image_dimensions(self.avatar)
            if w != 300:
                raise ValidationError('Please Make Width of Image 200')
            if h != 300:
                raise ValidationError('Please Make Height of Image 200')

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
