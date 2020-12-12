from django.urls import path
from .views import user_details, wall_details
from . import views

urlpatterns = [
	path('login/', views.login, name='adminlogin'),
	path('do-login/', views.do_login, name='do-login'),
	path('dashboard/', views.dashboard, name='admin-dashboard'),
	path('wall/<int:pk>/', wall_details.as_view(), name='admin-wall-details'),
	path('user/<int:pk>', user_details.as_view(), name='admin-user-details'),
	# path('')
]