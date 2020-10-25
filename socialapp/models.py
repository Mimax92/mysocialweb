from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Gossip(models.Model):
    content = models.TextField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="gossip_picture", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=25)


class Mesage(models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField(max_length=600)
    sender = models.ForeignKey(get_user_model(), related_name="sender", on_delete=models.SET_NULL, null=True,)
    receiver = models.ForeignKey(get_user_model(), related_name="receiver", on_delete=models.SET_NULL, null=True,)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    content =  models.TextField(max_length=200)
    sender = models.ForeignKey(get_user_model(), related_name="sender_not", on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(get_user_model(), related_name="receiver_not", on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gossip = models.ForeignKey(Gossip, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    gossip = models.ForeignKey(Gossip, on_delete=models.CASCADE, null=True)

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True, default="Warsaw")
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=35, null=True, blank=True)
    photo = models.ImageField(upload_to="user_picture", null=True, blank=True)