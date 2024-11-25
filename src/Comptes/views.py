
# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm, UserEditForm, VitrineForm
from .models import CustomUser, Vitrine


def inscription(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in after registration
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    users = CustomUser.objects.all()
    return render(request, 'home.html', {'form': form, 'users': users})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def edit_profile(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirection vers la page de profil après sauvegarde
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
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