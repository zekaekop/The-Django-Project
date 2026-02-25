from django.shortcuts import render, redirect , get_object_or_404, Http404
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from post.models import Post

from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator

from .models import UserProfile

def authenticate_users(request):
    if not request.user.is_authenticated:
        raise Http404()

# ----- Main Account logic -----
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else: # Login
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

            #site statistics displaying on the account creation page
            "total_accounts":accounts,
            "total_posts":posts,
            }
        
        return render(request, "account_templates/form.html", context)

def signin_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get('password')

        # create account
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False # If you need a superuser use 'python manage.py createsuperuser'
        user.save()
        new_user = authenticate(username = user.username, password = password)
        
        from procedural_pfp.views import PfpAssembly
        pfp_assembly = PfpAssembly()
        pfp_assembly.create_user_pfp(user, new_user) # create user PFP

        login(request, new_user)
        return redirect('/')
    
    posts = Post.objects.count()
    accounts = User.objects.count()
    
    context ={
        'form':form,
        'title':'Sign in',
        "donthaveaccount":False,
        
        #site statistics displaying on the account creation page
        "total_accounts":accounts,
        "total_posts":posts,
        }
        
    return render(request, "account_templates/form.html", context)

def increament_BZ(request, inc_amount):
    authenticate_users(request)
    user = request.user
    currency = UserProfile.objects.get(user=user)
    currency.BZ += inc_amount
    currency.save()

def decrease_BZ(request, dec_amount):
    authenticate_users(request)
    user = request.user
    currency = UserProfile.objects.get(user=user)
    if currency.BZ >= dec_amount:
        currency.BZ -= dec_amount
        currency.save()

# logs user out
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
