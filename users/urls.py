from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('user/sign_in/', auth_views.LoginView.as_view(template_name='users/sign_in.html', next_page="home"), name='login'),
    path('', views.home, name='home'),
    path('user/logout/', LogoutView.as_view(template_name='users/home.html'), name='logout'),
    path('user/register/', views.register, name='register'),
    path('user/show/<str:username>/', views.user_profile_page, name='user_profile_page'),
    path('user/edit', views.edit_profile_page, name='edit_profile_page'),
    path('user/edit/delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('friend_search', views.friend_search,name='friend_search'),
    path('follow_user/<str:username>', views.follow_user,name='follow_user'),
    path('unfollow_user/<str:username>', views.unfollow_user,name='unfollow_user'),
]


