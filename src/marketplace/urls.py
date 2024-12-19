
from django.urls import path

from shop.views import vitrine, create_vitrine, edit_vitrine, search_results, vitrine_detail, all_vitrines
from marketplace.views import create_marketplace, all_marketplace, CreateProduct,ProductDetail, add_to_cart, my_marketplace, cart_view,validate_cart_view,delete_product_from_cart, delete_cart



app_name = "marketplace"
urlpatterns = [


    #Search
    path('search/', search_results, name='search_results'),

    #Cart
    path("add_to_cart/<int:pk>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart"),
    path("validate_cart/", validate_cart_view, name="validate_cart"),
    path("delete_cart/<int:pk>", delete_cart, name="delete_cart"),



    #Marketplace
    path('all_marketplace/', all_marketplace, name='all_marketplace'),
    path("create_marketplace/", create_marketplace, name="create_marketplace"),
    path('my_marketplace/', my_marketplace, name='my_marketplace'),

    #Product
    path("create_product/", CreateProduct.as_view(), name="create"),
    path("delete_product/<int:pk>", delete_product_from_cart, name="delete_product"),
    path("<slug:slug>/", ProductDetail.as_view(), name="detail"),
]



