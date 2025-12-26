from urllib import request
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404, HttpResponse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse
from .models import Post, UserUpvote, UserReport
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from admin_panel.forms import ContactusForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import F

from django.core.paginator import Paginator
from django.conf import settings
#from django.utils.text import slugify

def authenticate_users(request):
    if not request.user.is_authenticated:
        raise Http404()

class Info:

    def about_us(request):
        return render(request, "info/about.html")

    def contact_us(request):
        form = ContactusForm(request.POST or None)

        if form.is_valid():
            contact = form.save(commit=False)

            # Attach user only if logged in
            if request.user.is_authenticated:
                contact.user = request.user

            contact.save()

            return render(
                request,
                "info/contact.html",
                {
                    "form": ContactusForm(),
                    "title": "Info",
                    "success": True,
                }
            )

        return render(
            request,
            "info/contact.html",
            {
                "form": form,
                "title": "Info",
            }
        )

class ListPosts():

    def posts_paginator(self, request):
        post_list = Post.objects.all()
        query = request.GET.get("q")

        if query: # Search query in header
            post_list = post_list.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)).distinct()
        paginator = Paginator(post_list, 9)  # Show 9 posts per page.
        page = request.GET.get("page")
        return paginator.get_page(page)
        
    def fetch_post_data(self, request, model): # Fetches upvotes and reports
        post_list = Post.objects.all()
        post_ids = post_list.values_list('id', flat=True)

        obj_qs = model.objects.filter(user=request.user, post_id__in=post_ids)
        return set(obj_qs.values_list('post_id', flat=True))

    def post_get_upvotes(self,request):
        return self.fetch_post_data( request,UserUpvote)
    
    def post_get_reports(self,request):
        return self.fetch_post_data(request,UserReport)
    
    def list_blog_posts(self,request):
        posts = self.posts_paginator(request)
        upvotes = self.post_get_upvotes(request)
        reports = self.post_get_reports(request)
        
        context = {
            "posts" : posts,
            "upvoted_posts" : upvotes,
            "reported_posts" : reports,
            "debug": settings.DEBUG,
        }

        suffix = ""
        for each_page in range(len(posts)):
            if len(posts[each_page].title) > 25:
                suffix = "..."
            else:
                suffix = ""
            posts[each_page].title = posts[each_page].title[:25] + suffix

        return render(request, "post_templates/index.html", context)
    
    def list_post_in_detail(self, request, id):
        post = get_object_or_404(Post, id = id)

        upvotes = self.post_get_upvotes(request)
        reports = self.post_get_reports(request)

        Post.objects.filter(id=post.id).update(post_views=F("post_views") + 1) # increases the post view by 1

        form = CommentForm(request.POST or None) # handles comment logic
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
        
        if post.user_html: has_html = True 
        else: has_html = False

        content = {
            "post" : post,
            "form" : form,
            "upvoted_posts" : upvotes,
            "reported_posts" : reports,
            "has_html" : has_html,
        }

        return render(request, "post_templates/detail.html", content)
    
    def render_web_view(self, *args, **kwargs):
        post = get_object_or_404(Post, id = kwargs.get("id"))
        if post.user_html:
            html_content = self.web_view(post) # Displays the html page with css js if there is
            return HttpResponse(html_content, content_type='text/html')
    
    def web_view(self, post):
        # Read html content
        html_path = post.user_html.path
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        html_content = self.web_view_file_includer(post, "user_css", "style","head", html_content)
        html_content = self.web_view_file_includer(post, "user_js", "script","body", html_content)
        return html_content
    
    def web_view_file_includer(self, post, file_type,file_format, in_element, html_content):
        
        if getattr(post,file_type):# checks if it exists
            path = getattr(post,file_type).path # Adds css and js files straight into one html file so i dont have to bother with multiple files
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read() # adds the js css contents at the end of their element tag ex. body or head
            return html_content.replace(f'</{in_element}>',f'<{file_format}>{content}</{file_format}>\n</{in_element}>',1)
        else:
            return html_content

class PostActions():

    def upvote_in_blog(self, request, id):
        self.upvote_post(request, id)
        page = request.GET.get("page", 1)
        return redirect(f"{reverse('post:index')}?page={page}")

    def upvote_in_detail(self, request, id):
        post = self.upvote_post(request, id)
        return redirect(post.get_absolute_url())

    def upvote_post(self, request, id):
        inc_type = "upvotes"
        self.increament_once_per_account(request, id, inc_type, UserUpvote)
        return redirect('post:index')


    def increament_once_per_account(self, request, id, inc_type, model):
        post = get_object_or_404(Post, id = id)

        authenticate_users(request)

        already_done = model.objects.filter(user = request.user,post=post)

        if already_done.exists():
            already_done.delete()
            Post.objects.filter(id=post.id).update(**{inc_type: F(inc_type) - 1})
        else:
            model.objects.create(user = request.user,post=post)
            Post.objects.filter(id=post.id).update(**{inc_type: F(inc_type) + 1})



    def post_report(self, request, id):
        inc_type = "reports"
        self.increament_once_per_account(request, id, inc_type, UserReport)
        return redirect('post:index')

    def post_delete(self, request, id):

        authenticate_users(request)

        deleted_post = get_object_or_404(Post, id = id)

        if deleted_post.user == request.user:
            deleted_post.delete()
            return redirect('post:index')
        else:
            raise Http404("cant delete wrong user")
        
    def post_update(self, request, id):

        authenticate_users(request)

        post = get_object_or_404(Post, id = id)

        if post.user == request.user or request.user.is_staff: # cant update posts if its a different user ... but if he is staff he can

            if request.method == "POST":
                action = request.POST.get("action")

                # Update text fields (fallback to old values)
                post.title = request.POST.get("title") or post.title
                post.desc = request.POST.get("desc") or post.desc

                # Update files ONLY if uploaded
                if request.FILES.get("site_preview"):
                    post.site_preview = request.FILES.get("site_preview")

                if request.FILES.get("user_html"):
                    post.user_html = request.FILES.get("user_html")

                if request.FILES.get("user_css"):
                    post.user_css = request.FILES.get("user_css")

                if request.FILES.get("user_js"):
                    post.user_js = request.FILES.get("user_js")

                if request.FILES.get("image"):
                    post.image = request.FILES.get("image")

                if request.FILES.get("video"):
                    post.video = request.FILES.get("video")

                if action == "publish":
                    if post.title and post.desc:
                        post.save()
                        return HttpResponseRedirect(post.get_absolute_url())

                if action == "preview":
                    return render(
                        request,
                        "post_templates/post_design_preview.html",
                        {"post": post}
                    )
            return render(request, "post_templates/create.html",{"post":post})
        else:
            raise Http404("cant update wrong user")


def post_create(request):
    authenticate_users(request)

    if request.method == "POST":
        action = request.POST.get("action")

        title = request.POST.get("title")
        desc = request.POST.get("desc")

        site_preview = request.FILES.get("site_preview")

        user_html = request.FILES.get("user_html")
        user_css = request.FILES.get("user_css")
        user_js = request.FILES.get("user_js")

        image = request.FILES.get("image")
        video = request.FILES.get("video")

        post = Post(
            user=request.user,
            title=title,
            desc=desc,
            image=image,
            video=video,
            site_preview=site_preview,
            user_html=user_html,
            user_css=user_css,
            user_js=user_js,
        )

        if action == "publish":
            if title and desc:
                post.save()
                return HttpResponseRedirect(post.get_absolute_url())

        if action == "preview":
            return render(request,"post_templates/post_design_preview.html",{"post": post})
        
    return render(request, "post_templates/create.html",{"title": "Create Post"})

def post_create_preview(request):
    if request.method == "POST":
        # Manually extract data from POST request
        title = request.POST.get('title')
        desc = request.POST.get('desc')

        image = request.POST.get('image')
        video = request.POST.get('video')
        site_preview = request.POST.get('site_preview')
        
        user_html = request.POST.get('user_html')
        user_css = request.POST.get('user_css')
        user_js = request.POST.get('user_js')
        site_preview = request.POST.get('site_preview')

        post = Post(
            user=request.user,
            title=title,
            desc=desc,

            image=image,
            video=video,
            site_preview=site_preview,

            user_html=user_html,
            user_css=user_css,
            user_js=user_js,
        )

        context = {
            "post" : post
        }

        return render(request, "post_templates/post_design_preview.html",context)
    post = Post(
        user=request.user,
        title="Title Example",
        desc="This is the Desc",
    )

    context = {
        "post" : post
    }

    return render(request, "post_templates/post_design_preview.html",context)