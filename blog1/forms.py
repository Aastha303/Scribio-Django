
from django import forms
from .models import Profile, Comment

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']

from .models import Blog

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']  # or whatever fields you use

