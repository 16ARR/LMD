
# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, UserEditForm
from .models import CustomUser


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
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirection vers la page de profil après sauvegarde
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
