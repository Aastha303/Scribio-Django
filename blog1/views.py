from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import TrendingBlog
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import ProfileUpdateForm, BlogPostForm
from .models import Blog
from django.conf import settings
import os
from blog1.models import Comment, Article, List, Post, RecommendedTopic, Writer  # Import all models correctly
from blog2.models import Follow

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render
from blog1.models import Blog

from django.db.models import Q

def search_view(request):
    query = request.GET.get('q', '')

    trending_blogs = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__icontains=query),
        is_trending=True
    )

    user_blogs = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__icontains=query),
        is_trending=False
    )

    return render(request, 'search_result.html', {
        'query': query,
        'trending_blogs': trending_blogs,
        'user_blogs': user_blogs,
    })



def index(request):
    # Get blogs by the current logged-in user
    my_blogs = Blog.objects.filter(author=request.user).order_by('-created_at')

    # Get trending posts
    trending_posts = TrendingBlog.objects.all()

    return render(request, 'index.html', {
        'my_blogs': my_blogs,
        'trending_posts': trending_posts
    })

def theme(request):
    return render(request, 'theme.html')

def rec_topic(request):
    return render(request, 'rec_topic.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful! Please Complete Your Profile.")

            if hasattr(user, 'role') and user.role == "admin":
                return redirect('badge')

            next_page = request.GET.get('next')
            return redirect(next_page) if next_page else redirect('index')

        else:
            messages.error(request, "Invalid credentials, please try again.")

    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Check for existing users
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose another one.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already used, please try with another one.")
        else:
            try:
                User.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password)
                )
                messages.success(request, "Registration successful! Please log in.")
                return redirect('login')
            except IntegrityError:
                messages.error(request, "An error occurred while creating your account.")

    return render(request, 'signup.html')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if current user is following this profile
        if self.request.user.is_authenticated:
            context['is_following'] = self.request.user.profile.is_following(self.get_object())
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile_edit.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    
@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login

def is_admin(user):
    return user.is_authenticated and user.profile.role == "admin"

@login_required
def admin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.profile.role == "admin":
                messages.success(request, "Login Successful! Please Complete Your Profile.")
                return redirect('badge')
            else:
                messages.error(request, "Access denied.")
        else:
            messages.error(request, "Access denied.")
    
    return render(request, 'admin.html')

def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)  # <-- Correct model reference
    if request.user == post.author or request.user.profile.role == 'admin':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this post.')
    return redirect('admin_view')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')  # or 'home' or wherever you want



from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # optional if using proper CSRF token in JS

@require_POST
@login_required
def toggle_follow(request, username):
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


def blog_list_view(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'damon', {'blogs': blogs})

def write_blog_view(request):
    if request.method == "POST":
        title = request.POST.get('title', 'Untitled Blog')
        content = request.POST.get('content', 'No content provided.')
        category = request.POST.get('category', 'Uncategorized')
        author = request.user.username if request.user.is_authenticated else "Damon"
        read_time = request.POST.get('read_time', 5)
        image = request.FILES.get('image')

        image_path = None
        if image:
            image_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join('uploads', image.name)
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

        Blog.objects.create(
            title=title,
            content=content,
            category=category,
            author=author,
            read_time=read_time,
            image_path=image_path
        )

        return redirect('index')

    return render(request, 'write_blog.html')


def blog_list_view(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog.html', {'blogs': blogs})


@login_required
def delete_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('index')
    return render(request, 'delete.html', {'blog': blog})

def submit_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        read_time = request.POST.get('read_time', 5)
        image = request.FILES.get('image')

        image_path = None
        if image:
            image_path = f"uploads/{image.name}"
            with open(f"static/{image_path}", 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

        blog = Blog.objects.create(
            title=title,
            content=content,
            category=category,
            read_time=read_time,
            author=request.user.username,
            image_path=image_path,
        )
        return redirect('index')
    
def submit_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        read_time = request.POST.get('read_time', 5)
        image = request.FILES.get('image')

        image_path = None
        if image:
            # Save the image to the media directory (using MEDIA_ROOT)
            image_path = f"uploads/{image.name}"
            image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            
            # Ensure the 'uploads' directory exists
            os.makedirs(os.path.dirname(image_full_path), exist_ok=True)

            # Save the image to the media directory
            with open(image_full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                    
        blog = Blog.objects.create(
            title=title,
            content=content,
            category=category,
            read_time=read_time,
            author=request.user.username,
            image_path=image_path,
        )
        return redirect('index')


def blog_detail_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'MEDIA_URL': settings.MEDIA_URL,
    })

def update_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category = request.POST.get('category')
        blog.read_time = request.POST.get('read_time', blog.read_time)

        image = request.FILES.get('image')
        if image:
            # Save the image to the media directory (using MEDIA_ROOT)
            image_path = f"uploads/{image.name}"
            image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            
            # Ensure the 'uploads' directory exists
            os.makedirs(os.path.dirname(image_full_path), exist_ok=True)

            # Save the image to the media directory
            with open(image_full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                    
            # Update the blog with the new image path
            blog.image_path = image_path

        blog.save()
        return redirect('blog_detail', blog_id=blog.id)

    return render(request, 'update_blog.html', {'blog': blog})



def blog_view(request):
    # Fetch recommended topics and writers from the database
    recommended_topics = RecommendedTopic.objects.all()
    writers = Writer.objects.all()

    # For debugging, check if the data is being fetched
    print("Recommended Topics:", recommended_topics)
    print("Writers:", writers)

    return render(request, 'blog.html', {
        'recommended_topics': recommended_topics,
        'writers': writers
    })



def damon(request):
    comments = Comment.objects.all().order_by('-date')
    articles = Article.objects.all().order_by('-date_posted')
    lists = List.objects.all().order_by('-date_created')
    posts = Post.objects.all().order_by('-date_posted')

    return render(request, 'damon.html', {
        'posts': posts,
        'comments': comments,
        'articles': articles,
        'lists': lists
    })

def add_comment(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        comment_content = request.POST.get('comment')
        post_id = request.POST.get('post_id')

        print("DEBUG: Received post_id =", post_id)  # Debugging post_id
        if not post_id:
            return HttpResponse("Missing post ID", status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return HttpResponse(f"Post with ID {post_id} does not exist", status=404)

        Comment.objects.create(author=author, content=comment_content, post=post, claps=0)
        return redirect('damon')  # After adding the comment, redirect to the damon page

def clap_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.claps += 1
    comment.save()
    
    return redirect('damon')  # Redirect to the damon view after clapping the comment