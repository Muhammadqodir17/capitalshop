from django.shortcuts import render


def contact_view(requests):
    return render(requests, 'contact.html')
