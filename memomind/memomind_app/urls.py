from django.conf import settings
from django.urls import path
from .views import *
from .views import LoginFormView, Logout
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # เส้นทางรากให้ชี้ไปที่ HomeView
    path('blog/register/', RegisterFormView.as_view(), name='register'),
    path('blog/login/', LoginFormView.as_view(), name='login'),  # URL สำหรับเข้าสู่ระบบ
    path('blog/create/', CreatePostView.as_view(), name='create_post'),
    path('blog/post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/profile/', ProfileView.as_view(), name='profile'),
    path('blog/favourites/', FavouriteView.as_view(), name='view_favourite'),
    path('blog/post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('blog/logout/', Logout.as_view(), name='logout'),  # URL สำหรับออกจากระบบ
    path('blog/post/<int:pk>/is_liked/', IsLikedView.as_view(), name='is_liked'),
    path('blog/post/<int:pk>/like/', LikePostView.as_view(), name='like_post'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)