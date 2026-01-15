from django.shortcuts import render, redirect , get_object_or_404, Http404
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from post.models import Post
from .models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
import random

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
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get('password')

        # create account
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        new_user = authenticate(username = user.username, password = password)

        create_user_profile(user, new_user)

        login(request, new_user)
        return redirect('/')
    
    posts = Post.objects.count()
    accounts = User.objects.count()
    
    context ={
        'form':form,
        'title':'Login',
        "donthaveaccount":False,
        "total_accounts":accounts,
        "total_posts":posts,
        }
        
    return render(request, "account_templates/form.html", context)

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

def create_user_profile(user, new_user):
    # generate pfp
    generated_pic_data = generate_profile_pic(4, 4)
    # Create UserProfile for the user
    UserProfile.objects.create(user=new_user, generated_pic=generated_pic_data)

def generate_profile_pic(height = 4, width = 4): # its 4 by 4 and than it gets mirrored and flipped on the other sides 

    generated_pic = []
    red = random.randint(128,255) # only 1 color for the entire thing
    blue = random.randint(128,255)
    green = random.randint(128,255)

    for y in range(height):
        row = []
        for x in range(width):
            if random.randint(1,2) == 1: # random 50% 50% to apply color or not
                row.append([red, blue, green, 255]) 
            else:
                row.append([0, 0, 0, 0]) 
        generated_pic.append(row)

    return generated_pic