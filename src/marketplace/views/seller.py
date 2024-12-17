from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from marketplace.models import Product


from marketplace.models import Product
from shop.models import Vitrine


class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "product/create_product.html"
    success_url = reverse_lazy("index")
    fields = ["titre", "price", "description", "category", "pics_1",
              "pics_2", "pics_3"]

    def form_valid(self, form):
        # Associer le produit à l'utilisateur
        form.instance.user = self.request.user

        # Associer le produit à la vitrine de l'utilisateur
        try:
            form.instance.vitrine = self.request.user.vitrine
        except Vitrine.DoesNotExist:
            # Si l'utilisateur n'a pas de vitrine, rediriger vers la création de vitrine
            from django.shortcuts import redirect
            return redirect('shop:create_vitrine')

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

def marketplace(request):
    products = Product.objects.filter(activate=True)
    sort_order = request.GET.get('sort', 'asc')

    if sort_order == 'asc':
        products = products.order_by('titre')
    elif sort_order == 'desc':
        products = products.order_by('-titre')

    return render(request, 'marketplace/marketplace.html', {'products': products})


def marketplace_vendeur(request, user_id):
    return Product.objects.filter(user=user_id)

