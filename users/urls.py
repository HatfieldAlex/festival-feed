from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('user/sign_in/', auth_views.LoginView.as_view(template_name='users/sign_in.html', next_page="home"), name='login'),
    path('', views.home, name='home'),
    path('user/logout/', LogoutView.as_view(template_name='users/home.html'), name='logout'),
    path('user/register/', views.register, name='register'),
]


