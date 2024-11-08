
# # VERSION 1
# from django.contrib import admin
#
# from django.urls import path
# from Comptes import views
# from django.contrib.auth import views as auth_views
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.home, name='home'),
#     path('profile/', views.profile, name='profile'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')
#
#
# ]
# VERSION 2
from django.contrib import admin

from django.urls import path
from shop.views import HomeView
from Comptes import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')


]