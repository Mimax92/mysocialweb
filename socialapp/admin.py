from django.contrib import admin
from .models import Gossip, Mesage, Notification, Like, Comment, Profile
# Register your models here.
admin.site.register(Gossip)
admin.site.register(Mesage)
admin.site.register(Notification)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)
