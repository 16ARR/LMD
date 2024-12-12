from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from marketplace.models import Product


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

class ProductDetail(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_object(self):
        # Obtenir l'article activé correspondant au slug
        return get_object_or_404(Product, slug=self.kwargs.get("slug"), activate=True)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["vitrine"] = self.object.user.vitrine  # Si "vitrine" est lié à l'utilisateur
    #     return context



# def marketplace(request):
#     query = request.GET.get('q', '')
#     if query:
#         products = Product.objects.filter(activate=True, titre__icontains=query)
#     else:
#         products = Product.objects.filter(activate=True)
#     return render(request, 'marketplace/marketplace.html', {'products': products, 'query': query})
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

