from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from .models import Blog, Comment
from .forms import BlogForm, CommentForm

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    blogs = Blog.objects.all().order_by('-published_date')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard.html', {'page_obj': page_obj})

@login_required
def new_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('dashboard')
    else:
        form = BlogForm()
    return render(request, 'new_blog.html', {'form': form})

@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.all()
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments})

@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect('blog_detail', slug=blog.slug)
    return redirect('blog_detail', slug=blog.slug)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog_detail', slug=comment.blog.slug)

@login_required
def search_blog(request):
    query = request.GET.get('query')
    blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-published_date')
    return render(request, 'search_results.html', {'blogs': blogs})

@login_required
def share_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        email = request.POST['email']
        send_mail(
            f"Check out this blog: {blog.title}",
            blog.content,
            'your_email@example.com',
            [email],
        )
        return redirect('dashboard')
    return render(request, 'share_blog.html', {'blog': blog})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.all()
    
    # Handle the form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect('blog_detail', slug=slug)  # Redirect to avoid resubmission

    else:
        comment_form = CommentForm()

    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})
