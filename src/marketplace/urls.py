
from django.urls import path

from shop.views import vitrine, create_vitrine, edit_vitrine, search_results, vitrine_detail, all_vitrines
from marketplace.views import CreateProduct,ProductDetail, marketplace, my_marketplace


app_name = "marketplace"
urlpatterns = [

    path("create_product/", CreateProduct.as_view(), name="create"),
    path("<slug:slug>/", ProductDetail.as_view(), name="detail"),
    path('', marketplace, name='marketplace'),
    path('my_marketplace/', my_marketplace, name='my_marketplace'),
    path('search/', search_results, name='search_results'),


]



