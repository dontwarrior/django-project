from django import views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  )

from .models import Post, Like


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user-post.html'
    context_object_name = 'posts'
    ordering_by = ['-likes_count']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['can_like'] = self.request.user != post.author.username
        context['has_liked'] = post.like_set.filter(user_id=self.request.user.id).exists()

        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html")


# def like_post(request, pk):
#     like = Like.objects.filter(user=request.user.id, post_id=pk).first()
#     post = Post.objects.get(pk=pk)
#     if like:
#         post.like.delete()
#         post.likes_count -= 1
#     else:
#         like = Like(test=str(pk), user=request.user)
#         like.post = post
#
#         post.save()
#         like.save()
#     return redirect('post-detail', pk)


class LikePostView(views.View):
    def get(self, request, **kwargs):
        current_user = request.user
        post = Post.objects.get(pk=kwargs['pk'])

        like = post.like_set.filter(user_id=current_user.id).first()
        if like:
            like.delete()
            post.likes_count -= 1
            post.save()
        else:
            like = Like(
                post=post,
                test='de',
                user=current_user
            )
            like.save()
            post.likes_count += 1
            post.save()

        return redirect('post-detail', post.id)
