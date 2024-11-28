from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserRegistrationForm, UserEditForm
from accounts.models import CustomUser

def user_logout(request):
    """Déconnecte l'utilisateur et le redirige vers la page d'accueil."""
    logout(request)
    return redirect("index")

def signup(request):
    """Inscription d'un nouvel utilisateur."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hachage du mot de passe
            user.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('accounts:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})  # Template spécifique à l'inscription

@login_required
def profile(request):
    """Affiche le profil de l'utilisateur."""
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    """Permet à l'utilisateur de modifier son profil."""
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')  # Redirection vers le profil après modification
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})
