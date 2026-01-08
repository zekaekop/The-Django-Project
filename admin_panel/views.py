from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404, HttpResponse
from info.models import ContactInfo
from post.models import Post
from django.contrib.auth.models import User
from .forms import ContactusForm

from .forms import AdminUsersPasswords

from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

# ----- Admin Panel Post Action logic -----

def delete_post_adminpanel(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_post = get_object_or_404(Post, id = id)

    if request.user.is_staff:
        deleted_post.delete()
        return redirect('/admin_panel/category/posts')

# ----- Admin Panel Contact Action logic -----

def delete_contact_adminpanel(request, id):

    if not request.user.is_authenticated:
        raise Http404()

    deleted_contact = get_object_or_404(ContactInfo, id = id)

    if request.user.is_staff:
        deleted_contact.delete()
        return redirect('/admin_panel/category/contacts')

def modify_contact_adminpanel(request, id):

    if not request.user.is_authenticated and not request.user.is_staff:
        raise Http404("not_athenticated")

    contact = get_object_or_404(ContactInfo, id = id)

    if contact.user == request.user or request.user.is_staff: # cant update posts if its a different user ... but if he is staff he can
        form = ContactusForm(request.POST or None, request.FILES or None, instance=contact)
        if form.is_valid():
            form.save()
            form.save()
            return  redirect('/admin_panel/category/contacts')
        
        context = {
            "title" : "Update Contact",
            "form" : form,
        }
        return render(request, "post_templates/form.html", context)
    else:
        raise Http404("cant update wrong user")
    

# ----- Displays Admin Panel Category Information -----

# ----- This is unused because i havent done the admin panel authentication system yet -----

def admin_panel(request):

    if request.user.is_staff or request.user.is_superuser:

        context = {"data_category":"default",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

def admin_panel_users(request):

    if request.user.is_staff or request.user.is_superuser:

        users_list = User.objects.all()

        query = request.GET.get("q")

        if query:
            users_list = users_list.filter(
                Q(username__icontains=query)).distinct()
        
        paginator = Paginator(users_list, 8)  # Show 8 per page.

        page = request.GET.get("page")
        users = paginator.get_page(page)
        
        context = {"admin_datas":users, "data_category":"users",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

def admin_panel_posts(request):

    if request.user.is_staff or request.user.is_superuser:

        post_list = Post.objects.all()

        query = request.GET.get("q")

        if query:
            post_list = post_list.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)).distinct()
    
        paginator = Paginator(post_list, 8)  # Show 8 per page.

        page = request.GET.get("page")
        posts = paginator.get_page(page)

        context = {"admin_datas":posts, "data_category":"posts",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

def admin_panel_contact(request):

    if request.user.is_staff or request.user.is_superuser:

        contacts_list = ContactInfo.objects.all()

        query = request.GET.get("q")

        if query:
            contacts_list = contacts_list.filter(
                Q(adress__icontains=query) |
                Q(email__icontains=query)|
                Q(name__icontains=query)|
                Q(surname__icontains=query)).distinct()
        
        paginator = Paginator(contacts_list, 8)  # Show 8 per page.

        page = request.GET.get("page")
        contacts = paginator.get_page(page)
            
        context = {"admin_datas":contacts, "data_category":"contacts",}

        return render(request, "account_templates/admin_panel.html", context)
    else:
        raise Http404()

# ----- Admin Panel User Action logic -----

def set_user_perms_staff_adminpanel(request, id):
    if request.user.is_staff:
        user = get_object_or_404(User, id = id)
        user.is_staff = not user.is_staff
        user.save()
    return redirect('/admin_panel/category/users')

def set_user_perms_superuser_adminpanel(request, id):
    if request.user.is_staff and request.user.is_superuser:
        user = get_object_or_404(User, id = id)
        user.is_superuser = not user.is_superuser
        user.save()
    return redirect('/admin_panel/category/users')

def active_state_user_account(request, id):
    if request.user.is_staff and request.user.is_superuser:
        user = get_object_or_404(User, id = id)
        user.is_active = not user.is_active
        user.save()
    return redirect('/admin_panel/category/users')

def password_change_user_account(request, id):
    user_id = get_object_or_404(User, id = id)
    user_form = AdminUsersPasswords(request.POST or None, instance=user_id) 

    if request.user.is_staff and request.user.is_superuser and user_form.is_valid():
        user = user_form.save(commit=False)
        new_password = user_form.cleaned_data.get("password")
        confirm = user_form.cleaned_data.get("confirm_password")

        if new_password and confirm and new_password == confirm:
            print(new_password)
            user.set_password(new_password)

        user.save()

        return redirect('/admin_panel/category/users')

    context = {
        "user_form" : user_form,
        "said_user" : user_id,
    }
            
    return render(request,'account_templates/change_user_password.html', context)