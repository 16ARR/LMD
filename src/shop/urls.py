

from django.urls import path

from shop.views import vitrine, create_vitrine, edit_vitrine, search_results, vitrine_detail, all_vitrines
app_name = "shop"
urlpatterns = [

    path('vitrine/', vitrine, name='vitrine'),
    path('create_vitrine/', create_vitrine, name='create_vitrine'),
    path('no_vitrine/', create_vitrine, name='vitrine_non_cree'),
    path('edit_vitrine/', edit_vitrine, name='edit_vitrine'),
    path('search/', search_results, name='search_results'),
    path('vitrine/<slug:slug_vitrine>/', vitrine_detail, name='vitrine_detail'),
    path('all_vitrines/', all_vitrines, name='all_vitrines'),
    path('vitrine_detail/', vitrine_detail, name='vitrine_detail'),




]