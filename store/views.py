import category
from django.shortcuts import render
from store.models import Product, Category


def home_view(requests):
    return render(requests, 'index.html')


def categories_view(requests):
    category = requests.GET.get('category')

    context = {
        'products': Product.objects.filter(category__name=category).order_by('-created_at')
    }
    return render(requests, 'categories.html', context=context)


def pages_view(requests):
    return render(requests, '...')
