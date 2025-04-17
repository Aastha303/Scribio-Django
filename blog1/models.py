from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class TrendingBlog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    read_time = models.IntegerField()
    author_image = models.CharField(max_length=255)  # You can use ImageField if you're handling uploads

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)  # Comma-separated
    is_profile_complete = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default_profile.jpg')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    
    def _str_(self):
        return f"{self.user.username}'s profile"
    
    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'username': self.user.username})
    
    def follow(self, profile):
        """Follow another user's profile"""
        if profile != self:  # Prevent self-following
            self.following.add(profile)
    
    def unfollow(self, profile):
        """Unfollow another user's profile"""
        self.following.remove(profile)
    
    def is_following(self, profile):
        """Check if this profile follows another profile"""
        return self.following.filter(pk=profile.pk).exists()
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()

# Signal to create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create an empty profile for the new user
        profile = Profile.objects.create(user=instance)
        
        # Ensure no automatic following happens here
        profile.following.clear()  # Clears any followers if it has been mistakenly added
        profile.save()

# Signal to save the profile when the user is saved or updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    read_time = models.IntegerField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_trending = models.BooleanField(default=False)  # Add this line
    tags = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    claps = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author}: {self.content[:50]}"
    
    @property
    def formatted_date(self):
        from datetime import datetime
        from django.utils.timezone import now
        delta = now() - self.date
        if delta.days > 30:
            return f"{delta.days // 30} months ago"
        elif delta.days > 0:
            return f"{delta.days} days ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hours ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return "Just now"

class Article(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class List(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StaticData(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    claps = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)
    read_time = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    claps = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
# Model for Recommended Topics
class RecommendedTopic(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'blog1_RecommendedTopic' 

    def __str__(self):
        return self.name

# Model for Writers
class Writer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='writers/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
