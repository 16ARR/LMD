from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Vitrine
from shop.forms import VitrineForm


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