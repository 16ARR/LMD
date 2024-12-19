from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from marketplace.models import Product, Order
from marketplace.forms import OrderForm


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

def marketplace(request):
    products = Product.objects.filter(activate=True)
    sort_order = request.GET.get('sort', 'asc')
    categories = set((product.get_category_display(), product.category) for product in products)
    # garments = {garment.category: garment.get_category_display()} categories = garments.keys()

    redirection = request.GET.get("category")
    if redirection:
        products = Product.objects.filter(category=redirection, activate=True)

    if sort_order == 'asc':
        products = products.order_by('titre')
    elif sort_order == 'desc':
        products = products.order_by('-titre')

    return render(request, "marketplace/marketplace.html", context={"products": products, "categories": categories})


def my_marketplace(request, user_id):
    return Product.objects.filter(user=user_id)

@require_POST
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, created = Order.objects.get_or_create(
        user=request.user,
        product=product,
        ordered=False
    )
    if not created:
        order.quantity += 1
        order.save()
    return redirect("marketplace:cart")

@login_required
def cart_view(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    OrderFormSet = modelformset_factory(Order, fields=("quantity",), extra=0)
    formset = OrderFormSet(queryset=orders)

    return render(request, "cart/cart.html", {"orders": orders, "formset": formset})

@require_POST
@login_required
def validate_cart_view(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        for order in orders:
            order.ordered = True
            order.save()
    return redirect("marketplace:marketplace")

@require_POST
@login_required
def delete_product_from_cart(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user, ordered=False)
    order.delete()
    return redirect("marketplace:cart")

@login_required
@require_POST
def delete_cart(request):
    request.user.cart.user_delete_cart()
    return redirect("marketplace:marketplace")

