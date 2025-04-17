# models.py (cleaned)

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class TrendingBlog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    read_time = models.IntegerField()
    author_image = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog2_profile')
    bio = models.TextField(blank=True, max_length=500)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default_profile.jpg')
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    is_profile_complete = models.BooleanField(default=False)
    following = models.ManyToManyField('self', symmetrical=False, related_name='blog2_followers', blank=True)
    followers = models.ManyToManyField(User, related_name='following_profiles', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile (blog2)"

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'username': self.user.username})

    def follow(self, profile):
        if profile != self:
            self.following.add(profile)

    def unfollow(self, profile):
        self.following.remove(profile)

    def is_following(self, profile):
        return self.following.filter(pk=profile.pk).exists()

    @property
    def followers_count(self):
        return self.blog2_followers.count()

    @property
    def following_count(self):
        return self.following.count()
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"