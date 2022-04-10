from dataclasses import field
import imp
from pyexpat import model
from webbrowser import get
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, RedirectView
from .models import Group, GroupMember
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.

#slug_field = 'slug' path <slug:slug>

class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','descripsion')
    model = Group

class SingleGroup(DetailView):
    model = Group

class ListGroup(ListView):
    model = Group

class JoinGroup (LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={ 'slug':self.kwargs.get('slug')})

    def get(self, request,*args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group = group)
        except IntegrityError:
            messages.warning(self.request,'Warning, Already a member of {}'.format(group.name))
        else:
            messages.success(self.request,'Now you are new member of {}'.format(group.name))
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={ 'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug = self.kwargs.get('slug')
            )
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'You are not in group!')
        else:
            membership.delete()
            messages.success(self.request,'Leave Group!')
        return super().get(request, *args, **kwargs)