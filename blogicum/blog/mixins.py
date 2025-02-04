from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail',
                        post_id=self.kwargs.get('post_id'))


class PostMixin:
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_field = 'comment_id'
    pk_url_kwarg = 'comment_id'

    def get_object(self):
        return get_object_or_404(
            Comment,
            pk=self.kwargs.get('comment_id'),
            post__id=self.kwargs.get('post_id'))

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs.get('post_id')})


class PostDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)
