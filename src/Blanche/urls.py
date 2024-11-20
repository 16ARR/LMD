from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path
from shop.views import HomeView
from Comptes import views
from django.contrib.auth import views as auth_views

from Comptes.user import exchanger_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('profile/', views.profile, name='profile'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', exchanger_logout, name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)