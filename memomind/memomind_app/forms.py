from django import forms
from .models import BlogPost, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [ 'image', 'categories','title', 'description']
        widgets = {
                'title': forms.TextInput(attrs={
                'class': 'bg-white shadow-md w-full px-3 py-2 border rounded mb-6'
                ,
                # 'placeholder': 'Title'
            }),
                'description': forms.Textarea(attrs={
                'class': 'w-full h-96 px-3 py-3 border rounded shadow ',
                'rows': 5,
                
            }),
                'categories': forms.CheckboxSelectMultiple(attrs={
                    'class': 'w-full px-3 py-12 border rounded text-xl text-softgreen focus:outline-none focus:ring focus:ring-brown' ,
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
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user