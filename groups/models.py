from django.urls import reverse

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

import misaka
# Create your models here

class Group(models.Model):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    descripsion = models.TextField(blank=True,default='')
    descripsion_html = models.TextField(editable=False,default='',blank=True)
    member = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        self.slug =slugify(self.name)
        self.descripsion_html = misaka.html(self.descripsion)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})
    
class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username