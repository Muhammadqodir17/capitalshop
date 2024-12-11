from django.urls import path
from .views import login_view, register_view, logout_view,profile_view, edit_profile_view


urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
]