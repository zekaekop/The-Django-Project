from django.shortcuts import render, redirect , get_object_or_404, Http404
from accounts.forms import LoginForm, RegisterForm, VerifyAccount
from django.contrib.auth.models import User
from post.models import Post , ContactInfo
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        login(request,user)
        return redirect('/')
    return render(request, "account_templates/form.html", {'form':form, 'title':'Login'})

def signin_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect('/')
    return render(request, "account_templates/form.html", {'form':form, 'title':'Sign in'})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def admin_panel(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404()

    admin_verify = VerifyAccount(request.POST or None, instance=request.user) 

    if request.method == "POST" and admin_verify.is_valid():
        verify = admin_verify.save(commit=False)

        password = admin_verify.cleaned_data.get("password")
        confirm = admin_verify.cleaned_data.get("confirm_password")

        if password and password == confirm:
            verify.set_password(password)
            verified = True
        else:
            verified = False
                
        verify.save()

        context = {
            "data_category": "default",
            "verified": verified,
            "form": admin_verify,
        }
        return render(request, "account_templates/admin_panel.html", context)
    return render(request, "account_templates/admin_panel.html", {"data_category": "default","verified": False, "form": admin_verify,})

def admin_panel_users(request):
    if request.user.is_staff or request.user.is_superuser:

        users = User.objects.all()

        query = request.GET.get("q")

        if query:
            users = users.filter(
                Q(username__icontains=query)).distinct()
            
        context = {"admin_datas":users, "verified": verified, "data_category":"users",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

def admin_panel_posts(request):

    if request.user.is_staff or request.user.is_superuser:

        posts = Post.objects.all()

        query = request.GET.get("q")

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)).distinct()
            
        context = {"admin_datas":posts, "verified": verified, "data_category":"posts",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

def admin_panel_contact(request):

    if request.user.is_staff or request.user.is_superuser:

        contacts = ContactInfo.objects.all()

        query = request.GET.get("q")

        if query:
            contacts = contacts.filter(
                Q(adress__icontains=query) |
                Q(email__icontains=query)|
                Q(name__icontains=query)|
                Q(surname__icontains=query)).distinct()
            
        context = {"admin_datas":contacts, "verified": verified, "data_category":"contacts",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

def set_user_perms_staff_adminpanel(request, id):
    
    if request.user.is_staff:
        user = get_object_or_404(User, id = id)
        user.is_staff = not user.is_staff
        user.save()
    
    return redirect('/accounts/admin_panel/users')

def set_user_perms_superuser_adminpanel(request, id):
    admin_verify = VerifyAccount(request.POST or None, instance=request.user) 
    password = admin_verify.cleaned_data.get("password")
    confirm = admin_verify.cleaned_data.get("confirm_password")

    if password == confirm:
        if request.user.is_staff and request.user.is_superuser:
            user = get_object_or_404(User, id = id)
            user.is_superuser = not user.is_superuser
            user.save()

    return redirect('/accounts/admin_panel/users')