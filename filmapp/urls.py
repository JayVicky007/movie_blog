from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name='home'),
    path('admin_posts/', views.admin_posts, name='admin_posts'),
    path('create/', views.create_blog, name='create_blog'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('guest/', views.guest_reviews, name='guest'),
    path('search/', views.search, name='search'),
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    

]

# Serve media files during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
