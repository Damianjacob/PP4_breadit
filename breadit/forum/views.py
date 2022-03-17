from genericpath import exists
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Post, Comment
from .forms import PostForm, EditPostform
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.


# Class-based view for the index page (which contains the posts)
class PostView(ListView):
    model = Post
    queryset = Post.objects.order_by('-created_on')
    post_list = queryset
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('created_on')
        return render(request, 'post_detail.html', {
            'post': post,
            'slug': slug,
            'comments': comments,
        })

# Class-based view for the creation of posts, limited to logged-in users
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'create_post_form.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        files = self.request.FILES
        # The following if statement checks if any new image was submitted,
        # and only tries to save that image  if that's the case.
        if 'post_file' in files:
            form.instance.image = files['post_file']

        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    # form_class = PostForm
    form_class = EditPostform
    model = Post
    template_name = 'update_post_form'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'update_post_form.html', {
            'post': post,
            'slug': slug
        })

    def form_valid(self, form):
        files = self.request.FILES
        # The following if statement checks if any new image was submitted,
        # and only tries to save a new image if that's the case.
        if 'post_file' in files:
            form.instance.image = files['post_file']
        form.save()
        return super().form_valid(form)

class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = '/'


class MyProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'profile'
    template_name = 'profile.html'
