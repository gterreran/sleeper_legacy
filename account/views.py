from django.shortcuts import render, redirect
# from django.contrib import messages
from django.contrib.auth import login, logout
from account.authentication import ExtendedAuthBackend
#from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

from .forms import UserSignupForm#, ForgottenPasswordForm, PasswordReset

def usersignup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'account/success.html')
        else:
            print('something went wrong')
    else:
        form = UserSignupForm()
    return render(request, 'account/signup.html', {'form': form})

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        user = ExtendedAuthBackend.authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
        if user is not None:
            login(request, user)
            # messages.success(request, 'Logged in successfully')
            return redirect('profile')
        # else:
        #     messages.error(request, 'Logged in Fail')
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {'form': form})

def userlogout(request):
    logout(request)
    return redirect('home')

# def forgotpassword(request):
#     if request.method == 'POST':
#         form = ForgottenPasswordForm(request.POST)
#         try:
#             user = User.objects.get(email=form["email"])
#         except User.DoesNotExist:
#             pass
#         return render(request, 'account/resetpasswordsent.html', {'email': form['email'].value})
#     else:
#         form = ForgottenPasswordForm()
#     return render(request, 'account/forgotpassword.html', {'form': form})

# def passwordreset(request):
#     if request.method == 'POST':
#         form = PasswordReset(request.POST)
#     else:
#         form = PasswordReset()
#     return render(request, 'account/forgotpassword.html', {'form': form})
