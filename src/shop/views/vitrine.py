from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from models import Vitrine


@login_required
def ma_vitrine(request):
    if not request.user.role == 'vendeur':
        return redirect('home')  # Redirige si l'utilisateur n'est pas vendeur
    try:
        vitrine = request.user.vitrine
        return render(request, 'ma_vitrine.html', {'vitrine': vitrine})
    except Vitrine.DoesNotExist:
        return render(request, 'vitrine_non_cree.html')

@login_required
def creer_vitrine(request):
    if not request.user.role == 'vendeur':
        return redirect('home')
    if request.method == 'POST':
        form = VitrineForm(request.POST)
        if form.is_valid():
            vitrine = form.save(commit=False)
            vitrine.user = request.user
            vitrine.save()
            return redirect('ma_vitrine')
    else:
        form = VitrineForm()
    return render(request, 'creer_vitrine.html', {'form': form})