from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import TrendingBlog, Profile, Follow  # ✅ Only import models once


# # ✅ Home view
# def home(request):
#     return HttpResponse("Welcome to the homepage!")


# ✅ Followers List
class FollowersListView(ListView):
    model = Profile
    template_name = 'followers_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return profile.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user__username=self.kwargs['username'])
        context['profile'] = profile

        current_user_profile = self.request.user.profile if self.request.user.is_authenticated else None

        for follower_profile in context['profiles']:
            follower_profile.is_following = (
                current_user_profile and current_user_profile.user in follower_profile.followers.all()
            )

        return context


# ✅ Following List
class FollowingListView(ListView):
    model = Profile
    template_name = 'following_list.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return profile.following.all()  # Assuming you have a `following` field on Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return context


# ✅ Toggle follow/unfollow
@login_required
def follow_toggle(request, username):
    """
    Toggle follow/unfollow a user
    """
    # Get the user to follow/unfollow
    user_to_follow = get_object_or_404(User, username=username)
    
    # Can't follow yourself
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect('profile_detail', username=username)
    
    # Check if already following
    try:
        # Assuming you have a Follow model with follower and following fields
        follow_obj = Follow.objects.get(follower=request.user, following=user_to_follow)
        # If exists, unfollow
        follow_obj.delete()
        messages.success(request, f"You have unfollowed {username}.")
    except Follow.DoesNotExist:
        # If not following, create follow relationship
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f"You are now following {username}.")
    
    # Redirect back to the profile page
    return redirect('profile_detail', username=username)

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received from JS:", data)

            user_message = data.get("message", "")

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": user_message,
                    "stream": False
                }
            )

            result = response.json()
            print("Ollama response:", result)

            return JsonResponse({"response": result.get("response", "Sorry, nothing to say.")})
        except Exception as e:
            print("🔥 Error in chatbot view:", e)
            return JsonResponse({"response": "Internal Server Error."}, status=500)

    return JsonResponse({"error": "POST required."}, status=405)

def chat_page(request):
    return render(request, "chat.html")
