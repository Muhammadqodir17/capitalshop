from django.db.models import Count
from django.shortcuts import render, redirect

from store.models import CardObj
from .models import Post, Category, Tag
from django.core.paginator import Paginator
from authentication.models import User
from blog.models import BlogComment


def blog_view(requests):
    user = requests.user

    if user.is_authenticated:
        auth_user = User.objects.filter(username=user).first()
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']

    else:
        auth_user = None
        cart_counter = 0

    cat = requests.GET.get('cat')
    tag_id = requests.GET.get('tag')
    tag = Tag.objects.filter(id=tag_id).first()
    if cat:
        posts = Post.objects.filter(category_id=cat, is_published=True)
    elif tag:
        posts = Post.objects.filter(tag=tag, is_published=True)
    else:
        posts = Post.objects.filter(is_published=True)

    paginator = Paginator(posts, 2)
    page_num = requests.GET.get('page')
    page = paginator.get_page(page_num)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular_posts = Post.objects.all().order_by('-view_count')[:4]
    d = {
        'posts': page,
        'auth': auth_user,
        'page': page,
        'categories': categories,
        'tags': tags,
        'popular_posts': popular_posts,
        'cart_num': cart_counter
    }
    return render(requests, 'blog.html', context=d)


def blog_detail_view(requests, pk):
    user = requests.user
    if user.is_authenticated:
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']
    else:
        cart_counter = 0

    if requests.method == 'POST':
        new_comment = BlogComment.objects.create(user=requests.user, post_id=pk, message=requests.POST.get('comment'))
        new_comment.save()
        blog_comment_count = Post.objects.filter(id=pk).first()
        blog_comment_count.comment_count += 1
        blog_comment_count.save()
        return redirect(f'/blog/blog/{pk}')

    tags = Tag.objects.all()
    categories = Category.objects.all()
    post = Post.objects.filter(id=pk, is_published=True).first()
    post.view_count += 1
    post.save(update_fields=['view_count'])
    popular_posts = Post.objects.all().order_by('-view_count')[:4]
    comments = BlogComment.objects.filter(post_id=pk)

    d = {
        'post': post,
        'tags': tags,
        'categories': categories,
        'popular_posts': popular_posts,
        'cart_num': cart_counter,
        'comments': comments,
    }
    return render(requests, 'blog-details.html', context=d)
