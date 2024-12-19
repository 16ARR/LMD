from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from marketplace.models import Product, Order




class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "product/create_product.html"
    success_url = reverse_lazy("index")
    fields = ["titre", "price", "description", "category", "pics_1",
              "pics_2", "pics_3"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductDetail(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_object(self):
        # Obtenir l'article activé correspondant au slug
        return get_object_or_404(Product, slug=self.kwargs.get("slug"), activate=True)





def search_results(request):
    query = request.GET.get('q')
    results = Product.objects.filter(
        Q(titre__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    ).distinct()
    return render(request, 'marketplace/search_results.html', {'query': query, 'results': results})



