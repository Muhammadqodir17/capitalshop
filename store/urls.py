from django.urls import path
from .views import home_view, categories_view

urlpatterns = [
    path('', home_view),
    path('category/', categories_view),
]
