from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from marketplace.models import Product


class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "product/create_product.html"
    success_url = reverse_lazy("index")
    fields = ["titre", "price", "description", "category", "pics_1",
              "pics_2", "pics_3"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
