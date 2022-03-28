from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register_view(request):
    '''
    Registers new users
    '''
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')
    return render(request, 'register.html', context={'form': form})


def login_view(request):
    '''
    Login users
    '''
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # redirect to the redirect url (the URL parameter "next") or to home page
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('/')
    return render(request, 'login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
