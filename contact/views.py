from django.shortcuts import render, redirect
from .models import Contact


def contact_view(requests):
    if requests.method == "POST":
        data = requests.POST

        obj = Contact.objects.create(name=data.get('name'), email=data.get('email'),
                                     subject=data.get('subject'), message=data.get('message'))
        obj.save()
        return redirect('/contact')
    return render(requests, 'contact.html')
