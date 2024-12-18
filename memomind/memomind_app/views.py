# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import BlogPost, Category, Comment
from .forms import BlogPostForm, CommentForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import BlogPost, Category
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BlogPostForm

class HomeView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        categories = Category.objects.all()
        selected_category = request.GET.get('category', 'all') 
        sort_option = request.GET.get('sort')  # Get the sorting option

        # Filter by category if not 'all'
        if selected_category != "all":
            posts = posts.filter(categories__name=selected_category)

        # Apply sorting
        if sort_option == 'newest':
            posts = posts.order_by('-created_at')  # Assuming 'created_at' is the field for post creation date
        elif sort_option == 'oldest':
            posts = posts.order_by('created_at')

        return render(request, 'index.html', {
            'posts': posts,
            'categories': categories,
            'selected_category': selected_category
        })


class LoginFormView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        print(form.errors)
        return render(request, "registration/login.html", {"form": form})
    
class RegisterFormView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "registration/register.html", {"form": form})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to home page after successful registration
        return render(request, "registration/register.html", {"form": form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        form = BlogPostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()  
            form.save_m2m() 
            return redirect('home')
        return render(request, 'create_post.html', {'form': form})


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        comments = post.comments.all()
        comment_form = CommentForm()
        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user  # เปลี่ยนเป็นผู้เขียนที่ลงชื่อเข้าใช้
            comment.save()
            return redirect('post_detail', pk=pk)
        return render(request, 'post_detail.html', {'post': post, 'comments': post.comments.all(), 'comment_form': comment_form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        liked_posts = user.liked_posts.all()
        posts = BlogPost.objects.filter(author=user)  

        return render(request, 'profile.html', {
            'liked_posts': liked_posts,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'profile_picture': user.profile.picture.url if hasattr(user, 'profile') else None,
            'posts': posts
        })
        
class FavouriteView(LoginRequiredMixin, View):
    def get(self, request):
        liked_posts = request.user.liked_posts.all()
        categories = Category.objects.all()

        # Set the default category to 'all'
        selected_category = request.GET.get('category', 'all')  # Default to 'all'
        
        # Filter liked posts if a specific category is selected (not 'all')
        if selected_category != "all":
            liked_posts = liked_posts.filter(categories__name=selected_category)

        # Get the sorting option
        sort_option = request.GET.get('sort')  # Get the sorting option

        # Apply sorting
        if sort_option == 'newest':
            liked_posts = liked_posts.order_by('-created_at')  # Assuming 'created_at' is the field for post creation date
        elif sort_option == 'oldest':
            liked_posts = liked_posts.order_by('created_at')

        return render(request, 'view_favourite.html', {
            'liked_posts': liked_posts,
            'categories': categories,
            'selected_category': selected_category  # Pass the selected category to the template
        })


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({'status': 'success'})
    
class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        if post.author == request.user:
            post.delete()
        return redirect('profile')
    
class IsLikedView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        is_liked = request.user in post.likes.all()
        return JsonResponse({'liked': is_liked})
