from django.urls import path, include
from .views import contact_view


urlpatterns = [
    path('', contact_view)
]