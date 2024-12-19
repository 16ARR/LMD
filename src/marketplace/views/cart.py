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