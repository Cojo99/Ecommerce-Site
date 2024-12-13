from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form.usable_password = None
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}!')
            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def profilepage(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    return redirect('store/home.html')

def profile_view(request):
    return render(request, 'store/home.html')