from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy # para quando apagarmos um post
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.
# Devolve, para um grupo ou utilizador, a lista dos posts
class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related=('user','group')

    queryset=models.Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        #context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
        context['all_groups'] = models.Group.objects.all()

        return context

class UserPosts(generic.ListView):
    model = models.Post
    template_name='posts/user_post_list.html'

    def get_queryset(self):
        try: #estamos agarrar o username do utilizador logado
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username')) #estamos a criar uma tributo da classe chamado post_user com a lista dos posts daquele utilizador
        except User.DoesNotExist: #atributo
            raise Http404 #nao estamos a chamar o metodo Http404(), apenas a levanta-lo
        else:
            return self.post_user.posts.all() # da variavel criada anteriormente devolvemos a lista de posts

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

        # get_context_data()
        # This method is used to populate a dictionary to use as the template
        # context. For example, ListViews will populate the result
        # from get_queryset() as author_list in the above example.
        # You will probably be overriding this method most often to add things
        # to display in your templates.
        # Neste caso, como estamos a herdar de uma view generica ListView,
        # queremos agarrar todo o seu dicionario de contexto e depois
        # customiza-lo com o novo campo que adicionamos post_user
        # no fundo estamos a disponibilizar para os templates do FE este novo atributo do dicionario context_Data

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

    # get_query_set()
    # Used by ListViews - it determines the list of objects that you want to display. By default it will just give you all for the model you specify. By overriding this method you can extend or completely replace this logic. Django documentation on the subject.
    #
    # class FilteredAuthorView(ListView):
    #     template_name = 'authors.html'
    #     model = Author
    #
    #     def get_queryset(self):
    #         # original qs
    #         qs = super().get_queryset()
    #         # filter by a variable captured from url, for example
    #         return qs.filter(name__startswith=self.kwargs.name)
    # Neste caso estamos a filtrar os posts de um determinado utilizador

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('message','group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
        # Este metodo atribui o post ao user logado

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id) # juser_id e ja um atributo da classe de que herdamos DeleteView

    def delete(self,*args,**kwargs): # numa deleteview esta a espera de ter este metodo, assim como o get_queryset
        messages.success(self.request,'Post Deleted') #framework do django para apresentar mensagens uma vez numa pagina, builtin
        return super().delete(*args,**kwargs)
