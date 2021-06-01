from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from accounts.forms import NewPostForm
from accounts.models import PostsModel, SocialConnectivity


def home(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("home")
    else:
        return render(request, "home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect('timeline')
    else:
        if request.method == "GET":
            form = UserCreationForm()
            return render(request, "register.html", {"form": form})
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    return redirect("login")
                except IntegrityError:
                    messages.error(request, "username already taken..")
                    return render(request, "register.html", {"form": UserCreationForm()})
            else:
                messages.error(request, "The two password fields didn't match.")
                return render(request, "register.html", {"form": UserCreationForm()})


def login(request):
    if request.user.is_authenticated:
        return redirect('todos')
    else:
        if request.method == "GET":
            form = AuthenticationForm()
            return render(request, "login.html", {"form": form})
        else:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is None:
                messages.error(request, "username and password didn't match")
                return render(request, "login.html", {"form": AuthenticationForm()})
            else:
                auth_login(request, user)
                return redirect("timeline")


def logout(request):
    auth_logout(request)
    return redirect("home")


@login_required
def timeline(request):
    user_obj = User.objects.get(id=request.user.id)
    followers = SocialConnectivity.objects.filter(follower=user_obj)
    follower_names = [i.following for i in followers]
    follower_names.append(user_obj)
    posts = PostsModel.objects.filter(created_by__in=follower_names)
    return render(request, "timeline.html", {"posts": posts})


@login_required
def profile(request):
    user_obj = User.objects.get(id=request.user.id)
    followers = SocialConnectivity.objects.filter(follower=user_obj)
    if request.method == "GET":
        return render(request, 'profile.html', {'user_data': user_obj, 'followers': len(followers)})
    else:
        if request.POST["first_name"]:
            user_obj.first_name = request.POST["first_name"]
        if request.POST["last_name"]:
            user_obj.last_name = request.POST["last_name"]
        if request.POST["email"]:
            user_obj.email = request.POST["email"]
        user_obj.save()
        messages.success(request, "Profile Updated Successfully.")
        return render(request, 'profile.html', {'user_data': user_obj, 'followers': len(followers)})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.created_by = request.user
            new_post.save()

            return redirect("timeline")
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})


def get_user_name(request):
    sq = request.GET.get('user_search')
    user_objects = [i.username for i in get_list_or_404(User, username__icontains=sq)]
    if user_objects:
        return JsonResponse(user_objects, safe=False)
    else:
        return JsonResponse({'status': 'false', 'message': "Not Found"}, status=404)


def find_friends(request):
    user_obj = User.objects.get(id=request.user.id)
    all_users = User.objects.all()

    followers = SocialConnectivity.objects.filter(follower=user_obj)
    followers_list = [i.following for i in followers]

    non_followers_list = [i for i in all_users if i not in followers_list]
    non_followers_list.remove(user_obj)
    return render(request, "find_friends.html", {"non_followers_list": non_followers_list})


def follow_user(request, name):
    usr_obj = User.objects.get(username=name)
    SocialConnectivity.objects.create(follower=request.user, following=usr_obj)
    return redirect("timeline")
