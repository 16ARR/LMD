from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from accounts.models import CustomUser
from shop.models import Vitrine
from shop.forms import VitrineForm, VitrineEditForm
from marketplace.models import Product

def search_results(request):
    query = request.GET.get('q')
    results = Vitrine.objects.filter(
        Q(nom_boutique__icontains=query) |
        Q(description_boutique__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()
    return render(request, 'shop/search_results.html', {'query': query, 'results': results})


def vitrine_detail(request, slug_vitrine, user_id):
    # Récupérer la vitrine à partir du slug
    vitrine = get_object_or_404(Vitrine, slug_vitrine=slug_vitrine)

    # Vérifier si l'utilisateur connecté est le propriétaire de la vitrine
    is_owner = (request.user == vitrine.user)

    # Récupérer l'utilisateur à partir de l'user_id
    user = get_object_or_404(CustomUser, id=user_id)

    # Obtenir les produits du vendeur correspondant au user_id et à la vitrine
    products = Product.objects.filter(user=user, activate=True)

    # Passer les données nécessaires au template
    return render(request, 'shop/vitrine_detail.html', {
        'vitrine': vitrine,
        'is_owner': is_owner,
        'products': products,
        'user': user,
    })





def all_vitrines(request):
    vitrines = Vitrine.objects.all()
    sort_order = request.GET.get('sort', 'asc')

    if sort_order == 'asc':
        vitrines = vitrines.order_by('nom_boutique')
    elif sort_order == 'desc':
        vitrines = vitrines.order_by('-nom_boutique')

    return render(request, 'shop/all_vitrines.html', {'vitrines': vitrines})


@login_required
def vitrine(request):
    if not request.user.role == 'vendeur':
        return redirect('home')  # Redirige si l'utilisateur n'est pas vendeur
    try:
        vitrine = request.user.vitrine
        return render(request, 'shop/vitrine.html', {'vitrine': vitrine})
    except Vitrine.DoesNotExist:
        return render(request, 'shop/no_vitrine.html')

@login_required
def create_vitrine(request):
    if not request.user.role == 'vendeur':
        return redirect('home')
    if request.method == 'POST':
        form = VitrineForm(request.POST)
        if form.is_valid():
            vitrine = form.save(commit=False)
            vitrine.user = request.user
            vitrine.save()
            return redirect('shop:vitrine')
    else:
        form = VitrineForm()
    return render(request, 'shop/create_vitrine.html', {'form': form})

@login_required
def edit_vitrine(request):
    """Permet à l'utilisateur de modifier sa vitrine."""
    vitrine = get_object_or_404(Vitrine, user=request.user)
    if request.method == 'POST':
        form = VitrineEditForm(request.POST, request.FILES, instance=vitrine)
        if form.is_valid():
            form.save()
            return redirect('shop:vitrine')  # Redirection vers la vitrine après modification
    else:
        form = VitrineEditForm(instance=vitrine)
    return render(request, 'shop/edit_vitrine.html', {'form': form})

