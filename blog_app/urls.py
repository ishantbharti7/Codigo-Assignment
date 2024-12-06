from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('new-blog/', views.new_blog, name='new_blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('search/', views.search_blog, name='search_blog'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('share/<slug:slug>/', views.share_blog, name='share_blog'),
]
