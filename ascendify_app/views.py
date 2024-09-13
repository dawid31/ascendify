from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout

def index(request):
    return render(request, 'ascendify_app/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Login failed. Check fields and try again.')

    return render(request, 'ascendify_app/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'ascendify_app/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('index')
