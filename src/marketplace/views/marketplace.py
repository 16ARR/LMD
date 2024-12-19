from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from marketplace.models import Marketplace, Product
from shop.models import Vitrine
from django.contrib import messages



@login_required
def my_marketplace(request):
    if not request.user.role == 'vendeur':
        return redirect('home')
    try:
        vitrine = request.user.vitrine
        try:
            # Vérifie si une marketplace est associée à la vitrine
            marketplace = vitrine.marketplace
            return render(request, 'marketplace/my_marketplace.html', {'marketplace': marketplace})  # Redirige vers la page de la marketplace existante
        except Marketplace.DoesNotExist:
            # Si pas de marketplace, affiche une page avec un bouton pour en créer une
            return render(request, 'marketplace/create_marketplace.html', {'vitrine': vitrine})
    except Vitrine.DoesNotExist:
        return render(request, 'shop/no_vitrine.html')

@login_required
def create_marketplace(request):
    try:
        # Vérifie si l'utilisateur a une vitrine
        vitrine = request.user.vitrine
        # Vérifie si une marketplace existe déjà pour cet utilisateur
        if hasattr(request.user, 'marketplace'):
            messages.info(request, "Vous avez déjà une marketplace.")
            return redirect('marketplace:ma_marketplace')

        # Crée une nouvelle marketplace associée à la vitrine
        marketplace = Marketplace.objects.create(
            user=request.user,
            vitrine=vitrine,
            statut=True
        )
        messages.success(request, "Votre marketplace a été créée avec succès.")
        return redirect('marketplace:my_marketplace')
    except Vitrine.DoesNotExist:
        messages.error(request, "Vous devez d'abord créer une vitrine avant de créer une marketplace.")
        return redirect('shop:no_vitrine')

def all_marketplace(request):
    products = Product.objects.filter(activate=True)
    sort_order = request.GET.get('sort', 'asc')
    categories = set((product.get_category_display(), product.category) for product in products)

    # Récupérer la catégorie sélectionnée
    selected_category = request.GET.get("category")
    if selected_category:
        products = products.filter(category=selected_category)

    # Trier les produits
    if sort_order == 'asc':
        products = products.order_by('titre')
    elif sort_order == 'desc':
        products = products.order_by('-titre')

    return render(request, "marketplace/all_marketplace.html", context={
        "products": products,
        "categories": categories,
        "selected_category": selected_category,  # Ajout de la catégorie sélectionnée
    })




