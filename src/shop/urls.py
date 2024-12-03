

from django.urls import path

from shop.views import vitrine, create_vitrine, edit_vitrine
app_name = "shop"
urlpatterns = [

    path('vitrine/', vitrine, name='vitrine'),
    path('create_vitrine/', create_vitrine, name='create_vitrine'),
    path('no_vitrine/', create_vitrine, name='vitrine_non_cree'),
    path('edit_vitrine/', edit_vitrine, name='edit_vitrine'),


]