from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from groups.models import Group,GroupMember
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model=Group

class ListGroups(generic.ListView):
    model=Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={"slug":self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request,*args,**kwargs)

        # get()
        # This is a top-level method, and there's one for each HTTP verb - get(), post(), patch(), etc. You would override it when you want to do something before a request is processed by the view, or after. But this is only called when a form view is loaded for the first time, not when the form is submitted. Basic example in the documentation. By default it will just render the configured template and return the HTML.
        #
        # class MyView(TemplateView):
        #     # ... other methods
        #
        #     def get(self, *args, **kwargs):
        #         print('Processing GET request')
        #         resp = super().get(*args, **kwargs)
        #         print('Finished processing GET request')
        #         return resp

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={"slug":self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(user=self.request.user,
                    group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group!')

        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')

        return super().get(request,*args,**kwargs)
