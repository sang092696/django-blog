from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import (ListView, 
    DetailView, #for class-based views
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] #newest to older post
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):   #overrides form valid view
        form.instance.author = self.request.user    #sets author of post to currently logged in user
        return super().form_valid(form) #runs form_valid method on parent class

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):   #overrides form valid view
        form.instance.author = self.request.user    #sets author of post to currently logged in user
        return super().form_valid(form) #runs form_valid method on parent class
    
    def test_func(self):
        post = self.get_object()    #gets post we are trying to update
        if self.request.user == post.author:    #checks if current logged in user is equal to author of post
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'   #sends user to homepage once deleted post

    def test_func(self):
        post = self.get_object()    #gets post we are trying to update
        if self.request.user == post.author:    #checks if current logged in user is equal to author of post
            return True
        return False



def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
