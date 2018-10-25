from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) # o parametro faz com que a data de criacaos eja automaticamente preenchida
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group,related_name="posts",on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk}) # quando e feito um post redireciona para o proprio post, ja publicado

        class Meta:
            ordering=['-created_at'] # - representa ordemd escendente: posts mais recentes em CsrfViewMiddleware
            unique_together = ['user','message']
