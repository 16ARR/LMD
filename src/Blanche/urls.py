from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Blanche import settings
from shop.views import index
from accounts.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("accounts/", include("accounts.urls")),
    path("shop/", include("shop.urls")),
    path("marketplace/", include("marketplace.urls")),
    path('profile/', profile, name='profile'),

]


