from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm #nao estamos a instanciar um objeto da classe, apenas a definir um atributo da classe SignUp como a outra classe que criamos no forms.py
    success_url =reverse_lazy('login') # usamos o reverse lazy porque so queremos este redirecionamento quando carregarem no botao de signup, o que aconteceria se usassemos apenas o reverse()
    template_name='accounts/signup.html'
