from django.shortcuts import render, redirect , get_object_or_404, Http404
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from post.models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

# ----- Main Account logic -----
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            login(request,user)
            return redirect('/')
        
        posts = Post.objects.count()
        accounts = User.objects.count()
        
        context ={
            'form':form,
            'title':'Login',
            "donthaveaccount":True,
            "total_accounts":accounts,
            "total_posts":posts,
            }
        
        return render(request, "account_templates/form.html", context)

def signin_view(request):
    form = RegisterForm(request.POST or None)
    
    posts = Post.objects.count()
    accounts = User.objects.count()
        
    context ={
        'form':form,
        'title':'Sign in',
        "donthaveaccount":False,
        "total_accounts":accounts,
        "total_posts":posts,
        }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists. Please choose a different one.')
            return render(request, "account_templates/form.html", context)
        if len(password) < 8:
            messages.warning(request, 'Password must be at least 8 characters long.')
            return render(request, "account_templates/form.html", context)
        user = form.save()
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect('/')
        
    return render(request, "account_templates/form.html", context)

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
