from store.utils import test_login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import UserCard
from django.contrib.auth.hashers import make_password

from .models import User
from store.models import CardObj, Order


def login_view(request):
    cart_counter = 0
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_for_username = authenticate(username=username, password=password)
        if user_for_username:
            login(request, user_for_username)
            return redirect(f'/{request.path[1:3]}/')
        return render(request, 'login.html', context={'message': 'Invalid username or password'})
    return render(request, 'login.html', context={'cart_num': cart_counter})


@test_login_required
def logout_view(request):
    logout(request)
    return redirect(f'/{request.path[1:3]}/')


def register_view(requests):
    if requests.method == "POST":
        data = requests.POST

        cart_counter = 0

        user_error = ''
        email_error = ''
        password_error = ''
        error_password = ''
        error_password2 = ''
        errors = 0

        username = data.get('username')
        data_email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        user = User.objects.filter(username=username).first()
        if user:
            user_error = 'User with this username already exist'
            errors += 1

        email = User.objects.filter(email=data_email).first()
        if email:
            email_error = 'Email with this email already exist'
            errors += 1

        if password != confirm_password:
            password_error = 'Password not match'
            errors += 1

        if not any(char.isdigit() for char in password):
            error_password = 'Password must include at least one number (0-9) or one special characters (_, .)'
            errors += 1

        if any(char in str(password) for char in '~`!@#$%^A&*()_+|}{[]\/:;",><?'):
            error_password2 = "Password contains invalid characters. Only _ and . are allowed as special characters."
            errors += 1

        if errors >= 1:
            d = {
                'cart_num': cart_counter,
                'user_error': user_error,
                'email_error': email_error,
                'password_error': password_error,
                'error_password': error_password,
                'error_password2': error_password2,
            }
            return render(requests, 'register.html', context=d)
        else:
            new_user = User.objects.create(username=username, email=data_email, password=make_password(password))
            new_user.save()

            return render(requests, 'login.html')
    return render(requests, 'register.html')


@test_login_required
def profile_view(request):
    cart_counter = CardObj.objects.filter(user=request.user, ordered=False).aggregate(Count('user'))['user__count']
    credit_cart = UserCard.objects.filter(user_id=request.user.id).first()
    if credit_cart is not None:
        card_num = str(credit_cart.pan)[-4:]
    else:
        card_num = 0
    orders = Order.objects.filter(user=request.user)

    d = {
        'user': request.user,
        'orders': orders,
        'credit_cart': credit_cart,
        'card_num': card_num,
        'cart_num': cart_counter
    }
    return render(request, 'profile.html', context=d)


def edit_profile_view(request):
    if request.method == 'POST':
        data = request.POST

        user = User.objects.filter(username=request.user).first()

        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        user.phone_number = data.get('phone_number')
        user.save()

    return redirect(f'/{request.path[1:3]}/auth/profile')
