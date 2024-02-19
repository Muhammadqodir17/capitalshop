from django.urls import path
from .views import blog_view, blog_detail_view

urlpatterns = [
    path('', blog_view),
    path('<int:pk>/', blog_detail_view),
]