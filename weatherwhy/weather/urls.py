from django.urls import path
from .views import index, register, user_login, user_logout, add_city, remove_city

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-city/', add_city, name='add_city'),
    path('remove-city/', remove_city, name='remove_city'),
]
