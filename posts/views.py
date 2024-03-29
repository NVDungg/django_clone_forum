from django.contrib import messages

from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from braces.views import SelectRelatedMixin
from soupsieve import select_one

from . import forms, models

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class PostList(SelectRelatedMixin,ListView):
    models = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        return models.Post.objects.all()

class UserPost(ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user 
        return context
    
class PostDetail(SelectRelatedMixin,DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    fields = ('message','group')
    model = models.Post

    def form_valid(self,form):
        self.objesct = form.save(commit=False)
        self.objesct.user = self.request.user
        self.objesct.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args, **kwargs):
        messages.success(self.request,'Post Delete')
        return super().delete(*args, **kwargs)