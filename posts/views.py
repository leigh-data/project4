from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Post
from .forms import PostForm

User = get_user_model()

class AllPostsView(ListView):
    queryset = Post.objects.all().prefetch_related('author').prefetch_related('liked_by')
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    http_method_names = ('post',)
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProfilePostsView(ListView):
    template_name = 'posts/profile.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.all().prefetch_related('liked_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = User.objects.get(username=self.kwargs['username'])
        context['profile_user'] = profile_user
        if profile_user and self.request.user.is_authenticated:
            context['following'] = profile_user in self.request.user.follows.all()
        else:
            context['following'] = False
        
        context['profile'] = True
        return context
    
    

class FollowingPostsView(LoginRequiredMixin, ListView):
    template_name = 'posts/following.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        follows = self.request.user.follows.all()
        return Post.objects.filter(author__in=follows).prefetch_related('author__posts').prefetch_related('liked_by')
