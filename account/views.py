from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import UserLoginForm, UserSignupForm

def userlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        user = authenticate(request, username=form["username"],
                            password=form["password"],
                            backend='account.authentication.ExtendedAuthBackend')
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Logged in Fail')
    return render(request, "account/login.html")

def usersignup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Process the form data here
            return render(request, 'account/success.html')
    else:
        form = UserSignupForm()
    return render(request, 'account/signup.html', {'form': form})

def forgotpassword(request):
    return render(request, 'account/forgotpassword.html')
