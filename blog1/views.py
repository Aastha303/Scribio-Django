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
from blog1.models import Comment, Article, List, Post, RecommendedTopic, Writer  
from blog2.models import Follow
import requests
from django.core.files.storage import FileSystemStorage
from django.views import View
from .models import Blog
from django.http import Http404


FLASK_API_BASE = getattr(settings, "FLASK_API_BASE", "http://127.0.0.1:5001")

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
    # Initialize empty lists for blogs
    my_blogs = []
    trending_blogs = []

    # Fetch regular blogs from Flask API
    try:
        flask_api_url = f"{FLASK_API_BASE}/api/blogs"
        response = requests.get(flask_api_url)

        print(f"Flask API Response Status: {response.status_code}")
        print(f"Flask API Response Content: {response.text[:100]}...")

        if response.status_code == 200:
            my_blogs = response.json()
        else:
            messages.error(request, "Failed to fetch blogs from Flask API.")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API request error for blogs: {e}")

    # Fetch trending blogs from Flask API
    try:
        trending_api_url = f"{FLASK_API_BASE}/api/trending-blogs"
        trending_response = requests.get(trending_api_url)

        print(f"Trending API Response Status: {trending_response.status_code}")
        print(f"Trending API Response Content: {trending_response.text[:100]}...")

        if trending_response.status_code == 200:
            trending_blogs = trending_response.json()
        else:
            messages.error(request, "Failed to fetch trending blogs from Flask API.")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API request error for trending blogs: {e}")

    return render(request, 'index.html', {
        'my_blogs': my_blogs,
        'trending_blogs': trending_blogs
    })


def theme(request):
    return render(request, 'theme.html')

def rec_topic(request):
    return render(request, 'rec_topic.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        payload = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(f"{FLASK_API_BASE}/login", json=payload)

            if response.status_code == 200:
                user_data = response.json()

                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={'email': user_data['email']}
                )

                user.set_password(password)
                user.save()

                user = authenticate(request, username=user_data['username'], password=password)

                if user is not None:
                    login(request, user)

                    request.session['username'] = user_data['username']
                    request.session['role'] = user_data['role']  

                    messages.success(request, "Login Successful!")
                    return redirect('index') 
                else:
                    messages.error(request, "Authentication failed.")
            else:
                error_msg = response.json().get("error", "Invalid credentials.")
                messages.error(request, error_msg)
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API error: {e}")
        except Exception as e:
            messages.error(request, f"Unexpected error: {e}")

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        payload = {
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": confirm_password
        }

        try:
            response = requests.post(f"{FLASK_API_BASE}/register", json=payload)

            if response.status_code == 200:
                user_data = response.json()
                messages.success(request, f"Welcome, {user_data['user']}!")
                return redirect('login')
            else:
                try:
                    error_msg = response.json().get("error", "Something went wrong.")
                except Exception:
                    error_msg = response.text
                messages.error(request, error_msg)

        except requests.exceptions.ConnectionError:
            messages.error(request, "Could not connect to the Flask API. Is it running?")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API request failed: {e}")

    return render(request, 'signup.html')

class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['username'] = self.object.username  
        

        try:
            response = requests.get(f"{FLASK_API_BASE}/profile/{self.request.user.username}")
            response.raise_for_status()
            profile_data = response.json()
            context['profile_data'] = profile_data
        except requests.exceptions.RequestException as e:
            context['error'] = f"Error fetching profile: {str(e)}"

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
    post = get_object_or_404(Blog, id=post_id)  
    if request.user == post.author or request.user.profile.role == 'admin':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this post.')
    return redirect('admin_view')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index') 



def blog_list_view(request):
    try:
        resp = requests.get(f"{settings.FLASK_API_BASE}/blogs", timeout=5)
        resp.raise_for_status()
        blogs = resp.json()               
    except requests.RequestException as e:
        raise Http404("Could not fetch blog list")


    request.session['blog_id_list'] = [b['id'] for b in blogs]

    return render(request, 'blog.html', {
        'blogs': blogs,
    })


@login_required
def write_blog_view(request):
    if request.method == "POST":

        title = request.POST.get('title', 'Untitled Blog')
        content = request.POST.get('content', 'No content provided.')
        category = request.POST.get('category', 'Uncategorized')
        author = request.user.username
        read_time = request.POST.get('read_time', 5)
        image = request.FILES.get('image')

        files = {}
        if image:
            files['image'] = (image.name, image.read(), image.content_type)

        data = {
            "title": title,
            "content": content,
            "category": category,
            "author": author,
            "read_time": read_time
        }

        access_token = request.session.get('access_token')  
        headers = {}
        if access_token:
            headers['Authorization'] = f"Bearer {access_token}"

        try:
            response = requests.post(
                f"{FLASK_API_BASE}/api/blogs/create",
                data=data,
                files=files,
                headers=headers
            )

            if response.status_code == 201:
                messages.success(request, "Blog created successfully .")
            else:
                messages.error(request, f"Failed to create blog. Status code: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API error: {e}")

        return redirect('index')
    

    return render(request, 'write_blog.html')

@login_required
def toggle_follow(request, username):
    """
    Toggle follow/unfollow a user
    """
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect('profile_detail', username=username)
    
    try:
        follow_obj = Follow.objects.get(follower=request.user, following=user_to_follow)
        follow_obj.delete()
        messages.success(request, f"You have unfollowed {username}.")
    except Follow.DoesNotExist:

        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f"You are now following {username}.")
    

    return redirect('profile_detail', username=username)

def blog_list_view(request):
    try:
        response = requests.get(f"{FLASK_API_BASE}/api/blogs")
        if response.status_code == 200:
            blogs = response.json()
        else:
            blogs = []
            messages.error(request, "Failed to load blogs from Flask backend.")
    except requests.exceptions.RequestException as e:
        blogs = []
        messages.error(request, f"Error contacting Flask API: {e}")

    return render(request, 'blog.html', {'blogs': blogs})

@login_required
def get_blog_by_id_view(request, blog_id):
    try:
        response = requests.get(f"{FLASK_API_BASE}/{blog_id}")
        
        if response.status_code == 200:
            blog = response.json()  
            return render(request, 'blog_detail.html', {'blog': blog})
        else:
            messages.error(request, "Blog not found")
            return redirect('index')
        
    except requests.exceptions.RequestException as e:
        messages.error(request, f"API error: {e}")
        return redirect('index')

@login_required
def delete_blog_view(request, blog_id):
    """
    Delete a blog post using the Flask API only.
    """
    try:
        response = requests.delete(f"{FLASK_API_BASE}/blogs/{blog_id}/delete")
        if response.status_code != 200:
            messages.error(request, f"Blog not found. Status code: {response.status_code}")
            return redirect('index')

        blog_data = response.json()

        if request.user.username == blog_data.get("author") or \
           (hasattr(request.user, 'profile') and request.user.profile.role == 'admin'):

            delete_response = requests.delete(f"{FLASK_API_BASE}/blogs/{blog_id}/delete")

            if delete_response.status_code == 200:
                messages.success(request, "Blog deleted successfully.")
            else:
                messages.error(request, f"Failed to delete blog. Status code: {delete_response.status_code}")
        else:
            messages.error(request, "Blog deleted successfully.")

    except requests.exceptions.RequestException as e:
        messages.error(request, f"API Error: {e}")

    return redirect('index')



@login_required
def submit_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled Blog')
        content = request.POST.get('content', 'No content provided.')
        category = request.POST.get('category', 'Uncategorized')
        author = request.user.username 
        read_time = request.POST.get('read_time', 5)
        image = request.FILES.get('image')

        files = {}
        if image:
            files['image'] = (image.name, image.read(), image.content_type)

        data = {
            "title": title,
            "content": content,
            "category": category,
            "author": author,
            "read_time": read_time
        }

        try:
            response = requests.post(f"{FLASK_API_BASE}/api/blogs/create", data=data, files=files)
            if response.status_code == 201:
                messages.success(request, "Blog submitted to Flask backend.")
            else:
                messages.error(request, f"Flask API error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Could not reach Flask API: {e}")

        return redirect('index')

    return render(request, 'write_blog.html')

def blog_detail_view(request, blog_id):
    try:
        from .models import Blog
        # Try fetching the blog from the Django database
        blog = Blog.objects.get(id=blog_id)
        
        # Prepare blog data for rendering in the template
        blog_data = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'category': blog.category,
            'author': str(blog.author),
            'read_time': blog.read_time,
            'image_path': blog.image_path,
            'is_django_blog': True  # Indicates this blog is from Django
        }
        
        return render(request, 'blog_detail.html', {
            'blog': blog_data,
            'MEDIA_URL': settings.MEDIA_URL,
        })
        
    except Blog.DoesNotExist:
        # If the blog doesn't exist in Django's database, fallback to Flask API
        try:
            # Adjusted API call for fetching blog from Flask API
            resp = requests.get(f"{FLASK_API_BASE}/detail/api/blog/{blog_id}", timeout=5)
            if resp.status_code == 200:
                blog = resp.json()
                blog['is_django_blog'] = False  # Mark this as a Flask blog
                return render(request, 'blog_detail.html', {
                    'blog': blog,
                    'MEDIA_URL': settings.MEDIA_URL,
                })
            else:
                raise Http404("Blog not found")
        except requests.RequestException:
            # If there's an error reaching Flask API
            raise Http404("Blog not found or API not reachable")




def update_blog_view(request, blog_id):
    try:
        # Adjusted URL for fetching blog details from Flask API
        res = requests.get(f"{FLASK_API_BASE}/api/blogs/{blog_id}")
        if res.status_code == 200:
            blog = res.json()
        else:
            raise Http404("Blog not found")
    except requests.exceptions.RequestException:
        raise Http404("Flask API unreachable")

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        read_time = request.POST.get('read_time', blog.get('read_time'))

        image = request.FILES.get('image')
        image_path = blog.get('image_path')
        if image:
            image_path = f"uploads/{image.name}"
            image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            os.makedirs(os.path.dirname(image_full_path), exist_ok=True)
            with open(image_full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

        payload = {
            "title": title,
            "content": content,
            "category": category,
            "read_time": read_time,
            "image_path": image_path,
            "author": request.user.username,
        }

        try:
            # Adjusted URL for updating blog via Flask API
            update_res = requests.put(f"{FLASK_API_BASE}/api/blog/update/{blog_id}", json=payload)
            if update_res.status_code == 200:
                return redirect('blog_detail', blog_id=blog_id)
            else:
                messages.error(request, "Update failed.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"API error: {e}")

    return render(request, 'update_blog.html', {'blog': blog})





def blog_view(request):
    recommended_topics = RecommendedTopic.objects.all()
    writers = Writer.objects.all()

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
        print("DEBUG: POST DATA= ",request.POST)
        author = request.POST.get('author')
        comment_content = request.POST.get('comment')
        post_id = request.POST.get('post_id')

        print("DEBUG: Received post_id =", post_id)  
        if not post_id:
            return HttpResponse("Missing post ID", status=400)
        
        payload = {
            "author": author,
            "comment":comment_content,
            "post_id":post_id
        }
        try:
            response = requests.post(f"{FLASK_API_BASE}/add_comments",json=payload)
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Failed to connect to Flask API: {e}", status=500)

        Comment.objects.create(author=author, content=comment_content, claps=0)
        return redirect('damon')  

def clap_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.claps += 1
    comment.save()
    
    return redirect('damon')