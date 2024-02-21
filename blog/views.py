from django.shortcuts import render
from .models import Post


def blog_view(requests):
    posts = Post.objects.filter(is_published=True)
    d = {
        'posts': posts,
    }
    return render(requests, 'blog.html', context=d)


def blog_detail_view(requests, pk):
    post = Post.objects.filter(id=pk, is_published=True).first()
    d = {
        'post': post,
        'tags': post.tag.all()
    }
    return render(requests, 'blog-details.html', context=d)