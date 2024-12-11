from django.db.models import Count
from django.shortcuts import redirect, render
from django.conf import settings

from store.models import CardObj
from .models import Contact
from authentication.models import User

BOT_ID = settings.BOT_ID
CHAT_ID = settings.CHAT_ID
TELEGRAM_API_URL = settings.TELEGRAM_API_URL


def contact_view(requests):
    user = requests.user
    if user.is_authenticated:
        auth_user = User.objects.filter(username=user).first()
        cart_counter = CardObj.objects.filter(user=user, ordered=False).aggregate(Count('user'))['user__count']

    else:
        auth_user = None
        cart_counter = 0

    if requests.method == 'POST':
        name = requests.POST.get('name')
        message = requests.POST.get('message')
        email = requests.POST.get('email')
        obj = Contact.objects.create(name=name, message=message, email=email)
        obj.save()

        message = (f"Project: Capital Shop\n"
                   f"name:{name}\n"
                   f"message:{message}\n"
                   f"email:{email}\n"
                   )

        requests.get(TELEGRAM_API_URL.format(BOT_ID, message, CHAT_ID))

        return redirect('/contact')
    return render(requests, 'contact.html', context={'auth': auth_user, 'cart_num': cart_counter
})

