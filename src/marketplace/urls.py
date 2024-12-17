
from django.urls import path

from shop.views import vitrine, create_vitrine, edit_vitrine, search_results, vitrine_detail, all_vitrines
from marketplace.views import CreateProduct,ProductDetail, marketplace, my_marketplace, add_to_cart, cart_view,validate_cart_view,delete_product_from_cart, delete_cart

app_name = "marketplace"
urlpatterns = [

    path("create_product/", CreateProduct.as_view(), name="create"),

    path('', marketplace, name='marketplace'),
    path('my_marketplace/', my_marketplace, name='my_marketplace'),
    path('search/', search_results, name='search_results'),

    path("add_to_cart/<int:pk>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart"),

    path("validate_cart/", validate_cart_view, name="validate_cart"),
    path("delete_product/<int:pk>", delete_product_from_cart, name="delete_product"),
    path("delete_cart/<int:pk>", delete_cart, name="delete_cart"),
    path("<slug:slug>/", ProductDetail.as_view(), name="detail"),



]



