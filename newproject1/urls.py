"""newproject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminsite/', include('administration.urls'), name='adminsite'),
    path('', include('wall.urls'), name='index'),
    path('register/', users_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='wall/index.html'), name='logout'),
    path('profile/', users_views.UserProfilePage, name='profile'),
    path('activate_premium/', users_views.go_premium, name='go-premium'),
    path('search/', users_views.search_user, name='search'),
    path('add/', users_views.add_user, name='add_user'),
    path('acc/', users_views.acc_user, name='acc_user'),
    path('get_friends/', users_views.get_friends, name='get_friends'),
    path('user-profile/<int:pk>/', users_views.friend_profile.as_view(), name='friend-profile'),
    path('edit/', users_views.editProfilePage, name='edit'),
    path('change-premium-status/', users_views.change_premium_status, name='change-premium-status'),
    path('privacy', users_views.privacypolicy, name='privacypolicy')
    # path('logout', auth_views.LoginView.as_view(), name='logout'),
]
