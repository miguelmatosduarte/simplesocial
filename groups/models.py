from django.db import models
from django.utils.text import slugify
from django import template
from django.urls import reverse

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()
register = template.Library()

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    # Quando se cria um grupo, para onde redirecionamos depois? Esta definido nesta classe
    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

class Meta:
    ordering= ['name']

# Esta classe e como se fosse apenas uma lookuptable em SQL com as relacoes N para N entre utilizadores e grupos
class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_groups",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')
