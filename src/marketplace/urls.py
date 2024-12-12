
from django.urls import path

from shop.views import vitrine, create_vitrine, edit_vitrine, search_results, vitrine_detail, all_vitrines
from marketplace.views import CreateProduct,ProductDetail

app_name = "marketplace"
urlpatterns = [

    path("create_product/", CreateProduct.as_view(), name="create"),
    path("<slug:slug>/", ProductDetail.as_view(), name="detail"),



]



