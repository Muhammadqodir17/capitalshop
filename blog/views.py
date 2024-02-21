from django.shortcuts import render, redirect
from .models import Post, Comment
from django.core.paginator import Paginator


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
    if requests.method == 'POST':
        data = requests.POST

        date = requests.GET
        cat = date.get('cat')
        page = date.get('page', 1)
        if cat:
            posts = Post.objects.filter(is_published=True, category_id=cat)
        else:
            posts = Post.objects.filter(is_published=True)

        paginator = Paginator(posts, 1)
        d = {
            'post': post,
            'tags': post.tag.all(),
            'paginator': paginator.page(page)
        }

        obj = Comment.objects.create(name=data['name'], email=data['email'], message=data['message'])
        obj.save()

        return redirect(f'/blog/{pk}')
    return render(requests, 'blog-details.html', context=d)