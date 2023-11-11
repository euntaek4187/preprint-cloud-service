from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages


def print_signup(req):
    if req.method == 'GET':
        form = SignUpForm()
        context = {'form': form}
        return render(req, 'accounts/print_signup.html', context)
    else:
        form = SignUpForm(req.POST)
        if form.is_valid():
            instance = form.save()
            return redirect('main')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] = 'error'  # This can highlight the input field with error
                for error in form[field].errors:
                    messages.error(req, error)
    context = {'form': form}
    return render(req, 'accounts/print_signup.html', context)
        
def print_login(req):
    if req.method == 'GET':
        return render(req, 'accounts/print_login.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(req, req.POST)
        if form.is_valid():
            login(req, form.user_cache) 
            return redirect('main')
        else:
            return render(req, 'accounts/print_login.html', {'form': form})

        
def print_logout(req):
    if req.user.is_authenticated:
        logout(req)
    return redirect('main')
    