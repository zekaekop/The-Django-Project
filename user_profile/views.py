from django.shortcuts import render, redirect
from user_profile.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from accounts.views import create_user_profile
from post.models import Post
from django.conf import settings
from django.core.paginator import Paginator

from friendship.models import FriendshipRequest
from friendship.models import Friend

from post.views import ListPosts

def authenticate_users(request):
    if not request.user.is_authenticated:
        raise Http404()

class ListProfilePage():

    def username_to_id(self, request, username):
        return User.objects.get(username=username)

    def current_profile_matches_req(self,request, user_profile):
        for req in Friend.objects.sent_requests(user=request.user):
            if req.to_user_id == user_profile.user.id:
                there_invite = True
                break
            else:
                there_invite = False
        
        return there_invite

    def profile(self, request, username):

        user = User.objects.get(username=username)
        user_posts_data = self.ListUserPosts(request, username)

        try:
            user_profile = UserProfile.objects.get(user=user) # if it doesnt exist than create it, support for older accounts that dont have this
        except UserProfile.DoesNotExist:
            user_profile = create_user_profile(user, user) 

        # profile = ProfileAssembly.profile_update(request)

        if username == request.user.username:
            pending_friend_req = Friend.objects.unrejected_requests(user=request.user)
        else:
            pending_friend_req = None # Dont display pending requests to other users
        
        other_user = self.username_to_id(request, username)
        
        if Friend.objects.are_friends(request.user, other_user):
            is_friend = True
        else:
            is_friend = False
        
        there_invite = self.current_profile_matches_req(request, user_profile)

        context = {
            "user": user,
            "profile":user_profile,
            "user_posts_data": user_posts_data,
            "pending_friend_req": pending_friend_req,
            "friends" : Friend.objects.friends(user), # displays the profile users friends
            "is_friend":is_friend,
            "friend_requested" :  there_invite,
            "user_id": self.username_to_id(request, request.user),
        }

        return render(request, "profile_templates/profile.html", context)

    def remove_friend(self, request, username):
        other_user = self.username_to_id(request, username)
        
        Friend.objects.remove_friend(request.user, other_user)
         # this may also work to remove pending requests
        return redirect("/profile/" + username)

    def cancel_friend_request(self, request, username):

        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        for req in Friend.objects.sent_requests(user=request.user):
            if req.to_user_id == user_profile.user.id:
                req.delete() # deletes friendship request, canceling the request
                break

        return redirect("/profile/" + username)

    def reject_friend_request(self, request, username):
        other_user = self.username_to_id(request, username)

        friend_request = FriendshipRequest.objects.get(
            from_user=other_user, to_user=request.user
        )

        friend_request.reject()
        return redirect("/profile/" + username)

    def accept_friend_request(self, request, username):
        other_user = self.username_to_id(request, username)

        friend_request = FriendshipRequest.objects.get(
            from_user=other_user, to_user=request.user
        )

        friend_request.accept()
        return redirect("/profile/" + request.user.username)

    def request_friend(self, request, username):
        other_user = self.username_to_id(request, username)
        
        Friend.objects.add_friend(
            request.user,  # The sender
            other_user,  # The recipient
            message=request.user.username,
        )  # This message is optional

        return redirect("/profile/" + username)

    def ListUserPosts(self,request, username):
        username_id =  self.username_to_id(request, username)
        post_list = Post.objects.filter(user=username_id)
        query = request.GET.get("q")

        if query: # Search query in header
            post_list = post_list.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)).distinct()
        paginator = Paginator(post_list, 9)  # Show 9 posts per page.te
        page = request.GET.get("page")

        posts = paginator.get_page(page)

        upvotes = ListPosts().post_get_upvotes(request)
        reports = ListPosts().post_get_reports(request)

        # category_activity = Post.objects.filter(category = category).count()

        context = {
            "posts" : posts,
            "upvoted_posts" : upvotes,
            "reported_posts" : reports,
            "debug": settings.DEBUG,
            # "category":Post.Categories,
            # "category_len":len(Post.Categories.choices),
            # "current_category": category,
            # "category_activity": category_activity,
        }

        suffix = "" # shortens the length of the title to prevent overflow
        for each_page in range(len(posts)):
            if len(posts[each_page].title) > 45:
                suffix = "..."
            else:
                suffix = ""
            posts[each_page].title = posts[each_page].title[:45] + suffix

        return context

    def change_credentials(self, request):
        if request.user.is_authenticated:
            name = {"name" : request.user.username}
            user_instance = request.user
        else:
            name = {"name" : "Guest",}


        user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_instance) 
            
        if user_form.is_valid():
            user = user_form.save(commit=False)

            new_password = user_form.cleaned_data.get("password")
            confirm = user_form.cleaned_data.get("confirm_password")

            if new_password and confirm and new_password == confirm:
                user.set_password(new_password)

            user.save()

            return redirect("/accounts/login")
        
        context = {
            "account": name,
            "user_form" : user_form,
        }
        
        return render(request, "profile_templates/change_credentials.html", context)

class ProfileEdit():

    def profile_update(self, request, username):
        user = User.objects.get(username=username)
        authenticate_users(request)

        try:
            userprofile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            userprofile = None

        context = {
            "user": user,
            "userprofile":userprofile,
        }

        if request.method == "POST":

            POST_data = self.get_profile_POST_data(request)
            profile = self.apply_profile_POST_data(request, POST_data, user)

            profile.user = request.user
            profile.save()
            return render(request, "profile_templates/profile_edit.html",context)

        return render(request, "profile_templates/profile_edit.html",context)
        
    def get_profile_POST_data(self, request): 
            return { # apperantly its better to do it with a dict instead of a class
                'bio': request.POST.get("bio"),
                'location': request.POST.get("location"),
                'user_age': request.POST.get("user_age"),
                'gender': request.POST.get("gender"),
                'image': request.FILES.get("image"),
            }
    
    def apply_profile_POST_data(self, request, POST_data, user):
        # POST_data is now a dictionary
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'bio': POST_data.get('bio', ''),
                'location': POST_data.get('location', ''),
                'user_age': POST_data.get('user_age'),
                'gender': POST_data.get('gender'),
            }
        )
        
        # If profile already existed, update its fields
        if not created:
            # Only update if the field is provided in POST_dataz
            if POST_data.get('bio') is not None:
                profile.bio = POST_data['bio']
            if POST_data.get('location') is not None:
                profile.location = POST_data['location']
            if POST_data.get('user_age') is not None:
                profile.user_age = POST_data['user_age']
            if POST_data.get('gender') is not None:
                profile.gender = POST_data['gender']
        
        # Handle image separately
        if POST_data.get('image'):
            profile.image = POST_data['image']

        if POST_data.get('user_age') == '':
            profile.user_age = None

        return profile