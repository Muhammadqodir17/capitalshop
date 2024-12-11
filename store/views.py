from django.core.paginator import Paginator
from django.db.models import Count, Sum
from decimal import Decimal, ROUND_DOWN

from django.urls import reverse

from authentication.models import CustomCard, UserCard

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.utils import json

from .models import Product, CardObj, LikedObj, Comment, Genre, Size, Color, Brand, Order, PromoCode, PromoCodeObj
from django.contrib.auth.decorators import login_required
from authentication.models import User
from blog.models import Post, Tag
from .utils import generate_qr_code


@login_required(login_url='/auth/login')
def wishlist_view(request):
    liked_obj = LikedObj.objects.filter(user=request.user)
    saved_cart = CardObj.objects.filter(user=request.user, ordered=False).values_list('product_id', flat=True)
    liked_product = LikedObj.objects.filter(user=request.user).values_list('product_id', flat=True)
    cart_counter = CardObj.objects.filter(user=request.user, ordered=False).aggregate(Count('user'))['user__count']

    d = {
        'liked_obj': liked_obj,
        'saved_cart': saved_cart,
        'liked_product': liked_product,
        'cart_num': cart_counter,
    }
    return render(request, 'wishlist.html', context=d)


def home_view(requests):
    user = requests.user
    if user.is_authenticated:
        auth_user = User.objects.filter(username=user).first()
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']

        liked_product = LikedObj.objects.filter(user=user).values_list('product_id', flat=True)
        saved_cart = CardObj.objects.filter(user=user, ordered=False).values_list('product_id', flat=True)
    else:
        auth_user = None
        liked_product = []
        saved_cart = []
        cart_counter = 0

    might_like_product = Product.objects.all().order_by('-rating')[:6]
    tag = Tag.objects.filter(name='Fashion Tips').first()
    latest_news_in_blog_fashion_tips = Post.objects.filter(tag=tag)

    products = Product.objects.all()

    for_men = Product.objects.filter(category=1).first()
    men = Product.objects.filter(category=1)

    for_women = Product.objects.filter(category=2).first()
    women = Product.objects.filter(category=2)

    for_baby = Product.objects.filter(category=3).first()
    babies = Product.objects.filter(category=3)

    context = {
        'products': products,
        'for_man': for_men,
        'men': men,
        'fashion_tips': latest_news_in_blog_fashion_tips,
        'auth': auth_user,
        'liked_product': liked_product,
        'saved_cart': saved_cart,
        'for_woman': for_women,
        'women': women,
        'for_baby': for_baby,
        'babies': babies,
        'cart_num': cart_counter,
        'might_like_product': might_like_product
    }
    return render(requests, 'index.html', context=context)


def men_products_view(requests):
    user = requests.user
    if user.is_authenticated:
        auth_user = User.objects.filter(username=user).first()
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']

        liked_product = LikedObj.objects.filter(user=user).values_list('product_id', flat=True)
        saved_cart = CardObj.objects.filter(user=user, ordered=False).values_list('product_id', flat=True)
    else:
        auth_user = None
        liked_product = []
        saved_cart = []
        cart_counter = 0

    sizes = Size.objects.all()
    colors = Color.objects.all()
    genres = Genre.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(category=1)

    if requests.method == 'POST':
        size = requests.POST.get('size')
        if size:
            products = products.filter(size__name=size)

        color = requests.POST.get('color')
        if color:
            products = products.filter(color__name=color)

        genre = requests.POST.getlist('genres')
        if genre:
            products = products.filter(genre__name__in=genre)

        brand = requests.POST.getlist('brands')
        if brand:
            products = products.filter(brand__name__in=brand)

        from_amount = requests.POST.get('from_amount')
        to_amount = requests.POST.get('to_amount')
        if from_amount or to_amount:
            products = products.filter(price__gte=from_amount, price__lte=to_amount)

    paginator = Paginator(products, 6)
    page_num = requests.GET.get('page', 1)
    page = paginator.get_page(page_num)

    context = {
        'auth': auth_user,
        'liked_product': liked_product,
        'saved_cart': saved_cart,
        'products': page,
        'sizes': sizes,
        'colors': colors,
        'genres': genres,
        'brands': brands,
        'cart_num': cart_counter,
    }
    return render(requests, 'categories.html', context=context)


def women_products_view(requests):
    user = requests.user
    if user.is_authenticated:
        auth_user = User.objects.filter(username=user).first()
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']

        liked_product = LikedObj.objects.filter(user=user).values_list('product_id', flat=True)
        saved_cart = CardObj.objects.filter(user=user, ordered=False).values_list('product_id', flat=True)
    else:
        auth_user = None
        liked_product = []
        saved_cart = []
        cart_counter = 0

    sizes = Size.objects.all()
    colors = Color.objects.all()
    genres = Genre.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(category=2)

    context = {
        'auth': auth_user,
        'liked_product': liked_product,
        'saved_cart': saved_cart,
        'products': products,
        'sizes': sizes,
        'colors': colors,
        'genres': genres,
        'brands': brands,
        'cart_num': cart_counter
    }
    return render(requests, 'categories.html', context=context)


def baby_products_view(requests):
    user = requests.user
    if user.is_authenticated:
        auth_user = User.objects.filter(username=user).first()
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']

        liked_product = LikedObj.objects.filter(user=user).values_list('product_id', flat=True)
        saved_cart = CardObj.objects.filter(user=user, ordered=False).values_list('product_id', flat=True)
    else:
        auth_user = None
        liked_product = []
        saved_cart = []
        cart_counter = 0

    sizes = Size.objects.all()
    colors = Color.objects.all()
    genres = Genre.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(category=3)

    context = {
        'auth': auth_user,
        'liked_product': liked_product,
        'saved_cart': saved_cart,
        'products': products,
        'sizes': sizes,
        'colors': colors,
        'genres': genres,
        'brands': brands,
        'cart_num': cart_counter
    }
    return render(requests, 'categories.html', context=context)


@login_required(login_url='/auth/login')
def product_detail_view(requests, pk):
    user = requests.user
    cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']
    rated_product = Comment.objects.filter(user=user).values_list('product_id', flat=True)
    product = Product.objects.filter(id=pk).first()
    saved_cart = CardObj.objects.filter(user=user, ordered=False).values_list('product_id', flat=True)

    num_rate_prod = Comment.objects.filter(product=product).aggregate(num_rate_prod=Count('rating'))
    full = int(product.rating)
    part = product.rating - full >= 0.5
    null = 5 - full
    if null == 1 and part:
        null = 0

    full_star_html = '<i class="fas fa-star"></i>' * full
    partial_star_html = '<i class="fas fa-star-half"></i>' if part else ''
    empty_star_html = '<i class="far fa-star"></i>' * null

    if user.is_authenticated:
        if requests.method == 'POST':
            data = requests.POST
            obj = Comment.objects.create(user=user, product=product, comment=data['message'], rating=data['rate'])
            product_average_rating = product.rating * product.rating_count + int(data['rate'])
            product.rating_count += 1
            product.rating = product_average_rating / product.rating_count
            product.save(update_fields=['rating', 'rating_count'])
            obj.save()

            return redirect(f'/store/product_detail/{pk}')
    else:
        return render(requests, 'login.html')

    comments = Comment.objects.filter(product=product)
    check_ordered = Order.objects.filter(product__id=pk).first()

    cur_product_rated = Comment.objects.filter(product__id=pk).first()
    cur_product_rated_full = int(cur_product_rated.rating)
    cur_product_rated_part = cur_product_rated.rating - cur_product_rated_full >= 0.5
    cur_product_rated_null = 5 - cur_product_rated_full
    if cur_product_rated_null == 1 and cur_product_rated_part:
        cur_product_rated_null = 0

    cur_product_rated_full_star_html = '<i class="fas fa-star"></i>' * cur_product_rated_full
    cur_product_rated_partial_star_html = '<i class="fas fa-star-half"></i>' if cur_product_rated_part else ''
    cur_product_rated_empty_star_html = '<i class="far fa-star"></i>' * cur_product_rated_null

    context = {
        'rated_product': rated_product,
        'num_rate': num_rate_prod,
        'saved_cart': saved_cart,
        'comments': comments,
        'full_star_html': full_star_html,
        'empty_star_html': empty_star_html,
        'partial_star_html': partial_star_html,
        'cur_product_rated_full_star_html': cur_product_rated_full_star_html,
        'cur_product_rated_partial_star_html': cur_product_rated_partial_star_html,
        'cur_product_rated_empty_star_html': cur_product_rated_empty_star_html,
        'product': product,
        'cart_num': cart_counter,
        'check_ordered': check_ordered,
    }
    return render(requests, 'pro-details.html', context=context)


@login_required(login_url='/auth/login')
def cart_view(requests):
    referer = requests.META.get('HTTP_REFERER')

    user = requests.user
    product_id = requests.GET.get('product_id')
    product = Product.objects.filter(id=product_id).first()
    exist = CardObj.objects.filter(user__username=user, product=product, ordered=False).first()

    if not exist:
        obj = CardObj.objects.create(
            user=user, name=product.name, product=product, price=product.price, discount=product.discount,
            price_with_discount=product.price_with_discount, quantity=1,
            total_price_with_discount=product.price_with_discount, total_price_without_discount=product.price)
        obj.save()
        obj.product.product_quantity -= 1
        obj.product.save()

    else:
        exist.quantity += 1
        exist.product.product_quantity -= 1
        exist.total_price_with_discount += product.price_with_discount
        exist.total_price_without_discount += product.price
        exist.save()
        exist.product.save()

    if referer == 'http://127.0.0.1:8000/store/men_products/':
        return redirect(f'/store/men_products/#{product_id}')
    elif referer == 'http://127.0.0.1:8000/store/women_products/':
        return redirect(f'/store/women_products/#{product_id}')
    elif referer == 'http://127.0.0.1:8000/store/baby_products/':
        return redirect(f'/store/baby_products/#{product_id}')
    elif referer == f'http://127.0.0.1:8000/store/product_detail/{product_id}':
        return redirect(f'/store/product_detail/{product_id}')
    else:
        return redirect(f'/store/#{product_id}')


@login_required(login_url='/auth/login')
def checkout_view(requests):
    if requests.method == 'POST':
        user = requests.user
        message = ''
        data = requests.POST

        promo = PromoCode.objects.filter(name=data.get('promo_code')).first()
        used_promo = PromoCodeObj.objects.filter(promo__name=data.get('promo_code'), user=requests.user).first()

        if data.get('promo_code') != '' and promo is None:
            card_objs = CardObj.objects.filter(user__username=user, ordered=False)
            cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))
            promo_not_exist_error = ''

            total_quantity = 0
            with_discount = 0
            without_discount = 0

            if card_objs:
                total_quantity = CardObj.objects.filter(user=user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0

                with_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
                    Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0

                without_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
                    Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0

                promo_not_exist_error = 'PromoCode is not exist'

            d = {
                'cart_num': cart_counter['user__count'],
                'total_quantity': total_quantity,
                'with_discount': with_discount,
                'without_discount': without_discount,
                'promo_not_exist_error': promo_not_exist_error,
            }
            return render(requests, 'checkout.html', context=d)
        elif data.get('promo_code') != '' and used_promo:
            card_objs = CardObj.objects.filter(user__username=user, ordered=False)
            cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))
            promo_used_error = ''

            total_quantity = 0
            with_discount = 0
            without_discount = 0

            if card_objs:
                total_quantity = CardObj.objects.filter(user=user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0

                with_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
                    Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0

                without_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
                    Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0

                promo_used_error = 'PromoCode already used'

            d = {
                'cart_num': cart_counter['user__count'],
                'total_quantity': total_quantity,
                'with_discount': with_discount,
                'without_discount': without_discount,
                'message': message,
                'promo_used_error': promo_used_error,
            }
            return render(requests, 'checkout.html', context=d)

        if data.get('delivery') == 'courier' and data.get('delivery_point') == '':
            user = requests.user
            card_objs = CardObj.objects.filter(user__username=user, ordered=False)
            cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))

            total_quantity = 0
            with_discount = 0
            without_discount = 0

            if card_objs:
                total_quantity = CardObj.objects.filter(user=user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0

                with_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
                    Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0

                without_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
                    Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0

                message = 'this field required'
            d = {
                'cart_num': cart_counter['user__count'],
                'total_quantity': total_quantity,
                'with_discount': with_discount,
                'without_discount': without_discount,
                'message': message,
            }
            return render(requests, 'checkout.html', context=d)

        if data.get('payment') == 'online':
            if data.get('delivery') == 'pickup':
                delivery = 1
            else:
                delivery = 2
            if data.get('payment') == 'byhand':
                payment = 1
            else:
                payment = 2
            product = CardObj.objects.filter(user=requests.user, ordered=False)
            product_quantity = CardObj.objects.filter(user=requests.user, ordered=False).aggregate(Sum('quantity'))['quantity__sum']
            total_price = CardObj.objects.filter(user=requests.user, ordered=False).aggregate(Sum('total_price_with_discount'))[
                'total_price_with_discount__sum']
            if data.get('promo_code') != '':
                order = Order.objects.create(
                    quantity=product_quantity,
                    total_price=total_price - ((total_price * promo.discount) / 100),
                    user=requests.user,
                    promo=PromoCode.objects.filter(name=data.get('promo_code')).first(),
                    delivery_address=data.get('delivery_address'), taking_type=delivery,
                    delivery_point=data.get('delivery_point'), first_name=data.get('first_name'),
                    last_name=data.get('last_name'), phone_number=data.get('phone_number'), email=data.get('email'),
                    payment_type=payment, payment_status=1
                )
                order.product.set(product.values_list('product', flat=True))
                order.save()
                new_promo = PromoCodeObj.objects.create(user=requests.user,
                                                        promo=PromoCode.objects.filter(
                                                            name=data.get('promo_code')).first())
                new_promo.save()
                for i in product:
                    if i.product.product_quantity == 0:
                        i.ordered = True
                        i.save()
                    elif i.quantity > i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.product.product_quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()
                    elif i.quantity < i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()

            else:
                order = Order.objects.create(
                    quantity=product_quantity,
                    total_price=total_price,
                    user=requests.user,
                    delivery_address=data.get('delivery_address'), taking_type=delivery,
                    delivery_point=data.get('delivery_point'), first_name=data.get('first_name'),
                    last_name=data.get('last_name'), phone_number=data.get('phone_number'), email=data.get('email'),
                    payment_type=payment, payment_status=1
                )
                order.product.set(product.values_list('product', flat=True))
                order.save()

                for i in product:
                    if i.product.product_quantity == 0:
                        i.ordered = True
                        i.save()
                    elif i.quantity > i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.product.product_quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()
                    elif i.quantity < i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()

            return render(requests, 'payment.html', context={'order_id': order.id})
        elif data.get('payment') == 'byhand':
            if data.get('delivery') == 'pickup':
                delivery = 1
            else:
                delivery = 2
            if data.get('payment') == 'byhand':
                payment = 1
            else:
                payment = 2

            product = CardObj.objects.filter(user=requests.user, ordered=False)
            product_quantity = CardObj.objects.filter(user=requests.user, ordered=False).aggregate(Sum('quantity'))['quantity__sum']
            total_price = CardObj.objects.filter(user=requests.user, ordered=False).aggregate(Sum('total_price_with_discount'))[
                'total_price_with_discount__sum']

            if data.get('promo_code') != '':
                order = Order.objects.create(
                    quantity=product_quantity,
                    total_price=total_price - ((total_price * promo.discount) / 100),
                    user=requests.user,
                    promo=PromoCode.objects.filter(name=data.get('promo_code')).first(),
                    delivery_address=data.get('delivery_address'), taking_type=delivery,
                    delivery_point=data.get('delivery_point'), first_name=data.get('first_name'),
                    last_name=data.get('last_name'), phone_number=data.get('phone_number'), email=data.get('email'),
                    payment_type=payment, payment_status=1
                )
                order.product.set(product.values_list('product', flat=True))
                order.save()
                generate_qr_code(order)
                new_promo = PromoCodeObj.objects.create(user=requests.user,
                                                        promo=PromoCode.objects.filter(
                                                            name=data.get('promo_code')).first())
                new_promo.save()

                for i in product:
                    if i.product.product_quantity == 0:
                        i.ordered = True
                        i.save()
                    elif i.quantity > i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.product.product_quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()
                    elif i.quantity < i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()

            else:
                order = Order.objects.create(
                    quantity=product_quantity,
                    total_price=total_price,
                    user=requests.user,
                    delivery_address=data.get('delivery_address'), taking_type=delivery,
                    delivery_point=data.get('delivery_point'), first_name=data.get('first_name'),
                    last_name=data.get('last_name'), phone_number=data.get('phone_number'), email=data.get('email'),
                    payment_type=payment, payment_status=1
                )
                order.product.set(product.values_list('product', flat=True))
                order.save()
                generate_qr_code(order)

                for i in product:
                    if i.product.product_quantity == 0:
                        i.ordered = True
                        i.save()
                    elif i.quantity > i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.product.product_quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()
                    elif i.quantity < i.product.product_quantity:
                        i.ordered = True
                        i.save()
                        obj = CardObj.objects.create(user=requests.user, product=i.product, name=i.product.name,
                                                     price=i.product.price,
                                                     discount=i.product.discount,
                                                     price_with_discount=i.product.price_with_discount,
                                                     quantity=i.quantity,
                                                     total_price_with_discount=i.product.product_quantity * i.product.price_with_discount,
                                                     total_price_without_discount=i.product.product_quantity * i.product.price)
                        obj.save()
                        qua = i.product.product_quantity
                        i.product.product_quantity -= qua
                        i.product.save()

            return redirect(reverse('profile'))
        else:
            return redirect('/checkout')

    user = requests.user
    card_objs = CardObj.objects.filter(user__username=user, ordered=False)
    cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))

    total_quantity = 0
    with_discount = 0
    without_discount = 0

    if card_objs:
        total_quantity = CardObj.objects.filter(user=user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0

        with_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
            Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0

        without_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
            Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0

    d = {
        'cart_num': cart_counter['user__count'],
        'total_quantity': total_quantity,
        'with_discount': with_discount,
        'without_discount': without_discount,
    }
    return render(requests, 'checkout.html', context=d)


@login_required(login_url='/auth/login')
def cart_obj_view(requests):
    user = requests.user
    card_objs = CardObj.objects.filter(user__username=user, ordered=False)
    cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))

    total_quantity = 0
    with_discount = 0
    without_discount = 0
    saving = 0

    if card_objs:
        total_quantity = CardObj.objects.filter(user=user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0

        with_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
            Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0

        without_discount = CardObj.objects.filter(user=user, ordered=False).aggregate(
            Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0

        saving = without_discount - with_discount

    auth_user = User.objects.filter(username=user).first()

    d = {
        'card_objs': card_objs,
        'auth': auth_user,
        'cart_num': cart_counter['user__count'],
        'total_quantity': total_quantity,
        'with_discount': Decimal(with_discount).quantize(Decimal('0.01'), rounding=ROUND_DOWN),
        'without_discount': Decimal(without_discount).quantize(Decimal('0.01'), rounding=ROUND_DOWN),
        'saving': Decimal(saving).quantize(Decimal('0.01'), rounding=ROUND_DOWN),
    }
    return render(requests, 'cart.html', context=d)


@login_required(login_url='/auth/login')
def like_obj_view(requests):
    referer = requests.META.get('HTTP_REFERER')

    product_id = requests.GET.get('product_id')
    user = requests.user

    product = Product.objects.filter(id=product_id).first()
    exist = LikedObj.objects.filter(user=user, product=product)
    if not exist:
        obj = LikedObj.objects.create(user=user, product=product)
        obj.save()
    else:
        exist.delete()

    if 'men_products' in referer:
        return redirect(f'/store/men_products/#{product_id}')
    elif 'women_products' in referer:
        return redirect(f'/store/women_products/#{product_id}')
    elif 'baby_products' in referer:
        return redirect(f'/store/baby_products/#{product_id}')
    elif f'/store/product_detail/{product_id}' in referer:
        return redirect(f'/store/product_detail/{product_id}')
    elif 'wishlist' in referer:
        return redirect('/store/wishlist')
    else:
        return redirect(f'/#{product_id}')


@login_required(login_url='/auth/login')
def update_cart_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])
    data = json.loads(request.body)
    cart_id = data.get('id')

    delta = -1 if data.get('sign') == '-' else 1

    try:
        cart_item = CardObj.objects.get(id=cart_id, user=request.user)
    except CardObj.DoesNotExist:
        return JsonResponse({"detail": "product not found"}, status=404)

    product = cart_item.product

    if delta == 1:  # Adding items to cart
        if product.product_quantity < delta:
            return JsonResponse({"detail": "Not enough stock available."}, status=400)

        # Decrease stock
        product.product_quantity -= delta
        product.save()
        cart_item.quantity += delta

    elif delta == -1:  # Removing items from cart
        if cart_item.quantity <= 1:  # Prevent negative quantity
            cart_item.quantity = 1

        # Increase stock
        product.product_quantity += 1
        product.save()
        cart_item.quantity -= 1

    # Update total prices after quantity change
    cart_item.total_price_with_discount = cart_item.price_with_discount * cart_item.quantity
    cart_item.total_price_without_discount = cart_item.price * cart_item.quantity
    cart_item.save()

    total_quantity = CardObj.objects.filter(user=request.user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0
    with_discount = CardObj.objects.filter(user=request.user, ordered=False).aggregate(
        Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0
    without_discount = CardObj.objects.filter(user=request.user, ordered=False).aggregate(
        Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0
    saving = without_discount - with_discount
    cart_counter = CardObj.objects.filter(user=request.user, ordered=False).aggregate(Count('user'))

    return JsonResponse(data={
        "count": cart_item.quantity,
        "price": {
            "with": cart_item.total_price_with_discount,
            "without": cart_item.total_price_without_discount,
            'total_quantity': total_quantity,
            'with_discount': with_discount,
            'without_discount': without_discount,
            'saving': saving,
            'cart_num': cart_counter['user__count'],
        }
    }, status=200)


@login_required(login_url='/auth/login')
def delete_cart_view(request, pk):
    cart = get_object_or_404(CardObj, id=pk)

    try:
        cart.product.product_quantity += cart.quantity
        cart.product.save()

        cart.delete()
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=400)

    cart_counter = CardObj.objects.filter(user=request.user, ordered=False).aggregate(Count('user'))['user__count']

    total_quantity = CardObj.objects.filter(user=request.user, ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0
    with_discount = CardObj.objects.filter(user=request.user, ordered=False).aggregate(
        Sum('total_price_with_discount'))['total_price_with_discount__sum'] or 0
    without_discount = CardObj.objects.filter(user=request.user, ordered=False).aggregate(
        Sum('total_price_without_discount'))['total_price_without_discount__sum'] or 0
    saving = without_discount - with_discount

    return JsonResponse(data={
        "message": "success",
        "cart": {
            "cart_num": cart_counter,
            'total_quantity': total_quantity,
            'with_discount': with_discount,
            'without_discount': without_discount,
            'saving': saving,
        }
    }, status=200)


def pay_online_view(request, pk):
    if request.method == 'POST':
        data = request.POST
        check = 0

        pan_not_found_error = ''
        expired_month_error = ''
        expired_year_error = ''
        cvv_error = ''
        expired_month_not_match_error = ''

        pan = CustomCard.objects.filter(pan=data.get('card_number')).first()

        if pan is None:
            pan_not_found_error = 'Card not found'
            check += 1

        if pan is not None and int(data.get('expire_month')) > 12:
            expired_month_error = 'it must be exist month: 1 to 12'
            check += 1
        if pan is not None and int(data.get('expire_month')) != pan.expired_month:
            expired_month_not_match_error = 'Month is not match'
            check += 1

        created_year = CustomCard.objects.filter(pan=data.get('card_number')).first()
        if pan is not None and int(data.get('expire_year')) > created_year.expired_year or int(
                data.get('expire_year')) < created_year.expired_year:
            expired_year_error = 'The card has expired'
            check += 1

        cvv = CustomCard.objects.filter(cvv=data.get('cvv')).first()
        if pan is not None and cvv is None:
            cvv_error = "Card's cvv is incorrect "
            check += 1

        if check >= 1:
            d = {
                'pan_not_found_error': pan_not_found_error,
                'expired_month_error': expired_month_error,
                'expired_year_error': expired_year_error,
                'cvv_error': cvv_error,
                'expired_month_not_match_error': expired_month_not_match_error,
                'order_id': pk,
            }
            return render(request, 'payment.html', context=d)
        else:
            usercard = UserCard.objects.filter(user_id=request.user.id, pan=data.get('card_number'),
                                               expired_month=data.get('expire_month'),
                                               expired_year=data.get('expire_year'), cvv=data.get('cvv')).first()
            if usercard:
                order_payed = Order.objects.filter(id=pk, user=request.user).first()
                usercard.balance -= order_payed.total_price
                order_payed.payment_status = 2
                order_payed.save()
                usercard.save()
                card = CustomCard.objects.filter(pan=data.get('card_number'),
                                                 expired_month=data.get('expire_month'),
                                                 expired_year=data.get('expire_year'), cvv=data.get('cvv')).first()
                card.balance = usercard.balance
                card.save()
                generate_qr_code(order_payed)

                return redirect(reverse('profile'))
            else:
                card = CustomCard.objects.filter(pan=data.get('card_number'),
                                                 expired_month=data.get('expire_month'),
                                                 expired_year=data.get('expire_year'), cvv=data.get('cvv')).first()
                order_payed = Order.objects.filter(id=pk, user=request.user).first()
                card.balance -= order_payed.total_price
                order_payed.payment_status = 2
                order_payed.save()
                card.save()
                generate_qr_code(order_payed)

                return redirect(reverse('profile'))
    return render(request, 'payment.html', context={'order_id': pk})


@login_required(login_url='/auth/login')
def delete_order_view(request, pk):
    order = get_object_or_404(Order, id=pk)
    if order.promo is not None:
        used_promo = PromoCodeObj.objects.filter(user_id=request.user.id, promo__name=order.promo.name).first()
        used_promo.delete()

    for i in order.product.all():
        card = CardObj.objects.filter(user__id=request.user.id, product__id=i.id, ordered=False).first()
        if card is None:
            ordered_true = CardObj.objects.filter(user__id=request.user.id, product__id=i.id, ordered=True)
            quantity = ordered_true.aggregate(Sum('quantity'))['quantity__sum'] or 0
            new_cart = CardObj.objects.create(user=request.user, product=i, name=i.name, price=i.price, discount=i.discount,
                                              price_with_discount=i.price - ((i.discount / 100) * i.price), quantity=quantity, total_price_with_discount=(i.price * quantity) - ((i.discount / 100) * i.price),
                                              total_price_without_discount=i.price * quantity
                                              )
            new_cart.save()
            ordered_true.delete()
        else:
            ordered_true = CardObj.objects.filter(user__id=request.user.id, product__id=i.id, ordered=True)
            quantity = ordered_true.aggregate(Sum('quantity'))['quantity__sum'] or 0
            card.quantity = quantity
            card.total_price_with_discount = quantity * card.price_with_discount
            card.total_price_without_discount = quantity * card.price
            card.save()
            ordered_true.delete()

    try:
        order.delete()
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=400)
    return JsonResponse(data={
        "message": "success",
    }, status=200)


def add_card_view(request):
    return render(request, 'add_card.html')


def add_card_details_view(request):
    if request.method == 'POST':
        data = request.POST
        check = 0

        pan_not_found_error = ''
        expired_month_error = ''
        expired_year_error = ''
        cvv_error = ''
        expired_month_not_match_error = ''

        pan = CustomCard.objects.filter(pan=data.get('card_number')).first()

        if pan is None:
            pan_not_found_error = 'Card not found'
            check += 1

        if pan is not None and int(data.get('expire_month')) > 12:
            expired_month_error = 'it must be exist month: 1 to 12'
            check += 1
        if pan is not None and int(data.get('expire_month')) != pan.expired_month:
            expired_month_not_match_error = 'Month is not match'
            check += 1

        created_year = CustomCard.objects.filter(pan=data.get('card_number')).first()
        if pan is not None and int(data.get('expire_year')) > created_year.expired_year:
            expired_year_error = 'The card has expired'
            check += 1

        cvv = CustomCard.objects.filter(cvv=data.get('cvv')).first()
        if pan is not None and cvv is None:
            cvv_error = "Card's cvv is incorrect "
            check += 1

        if check >= 1:
            d = {
                'pan_not_found_error': pan_not_found_error,
                'expired_month_error': expired_month_error,
                'expired_year_error': expired_year_error,
                'cvv_error': cvv_error,
                'expired_month_not_match_error': expired_month_not_match_error,
            }
            return render(request, 'add_card.html', context=d)
        else:
            custom_card = CustomCard.objects.filter(pan=data.get('card_number'), expired_month=data.get('expire_month'),
                                                    expired_year=data.get('expire_year'), cvv=data.get('cvv')).first()
            user_card = UserCard.objects.create(user=request.user, first_name=custom_card.first_name,
                                                last_name=custom_card.last_name,
                                                pan=custom_card.pan, cvv=custom_card.cvv,
                                                bank_name=custom_card.bank_name,
                                                card_name=custom_card.card_name, phone_number=custom_card.phone_number,
                                                balance=custom_card.balance, created_month=custom_card.created_month,
                                                created_year=custom_card.created_year,
                                                expired_month=custom_card.expired_month,
                                                expired_year=custom_card.expired_year)
            user_card.save()
    return redirect(reverse('profile'))


def exit_card_view(request, pk):
    user_card = UserCard.objects.filter(id=pk).first()
    if user_card:
        user_card.delete()

    return redirect(reverse('profile'))


def support_view(request):
    return render(request, 'support.html')


def faq_view(request):
    return render(request, 'faq.html')


def privacy_view(request):
    return render(request, 'privacy')


def about_view(request):
    return render(request, 'about.html')


def search_view(request):
    return render(request, 'categories.html')
