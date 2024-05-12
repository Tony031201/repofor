from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .forms import LoginForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get("password")

        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('index')

    context = {
        'form':form
    }

    return render(request,'users/login.html',context)


def register_view(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = form.save()
        login(request,user)
        return redirect('index')
    else:
        form = UserCreationForm()

    context = {
        'form':form
    }

    return render(request, 'users/register.html', context)

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    messages.success(request,"You logged Out.")
    return redirect('index')