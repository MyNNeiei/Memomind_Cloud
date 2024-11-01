from django import forms
from .models import BlogPost, Comment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'image', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50',
                'placeholder': 'Enter post title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50',
                'placeholder': 'Write your post description here'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'mt-1',
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50',
                'rows': 4,
                'placeholder': 'Add your comment here'
            }),
        }
