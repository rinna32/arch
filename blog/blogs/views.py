from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import Http404,HttpResponseForbidden
from .models import BlogPost, Entry
from .forms import BlogForm, EntryForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    """Домашняя страница приложения Learning Log"""
    posts = None
    if request.user.is_authenticated:
        posts = BlogPost.objects.all().order_by('-date_added')[:5]
    latest_posts = BlogPost.objects.order_by('-date_added')[:3]
    return render(request, 'blogs/index.html')
@login_required
def posts(request):
    """Выводит список всех блог-постов."""
    posts = BlogPost.objects.filter(owner=request.user).order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)
@login_required
def post(request, post_id):
    """Выводит один пост и все его записи."""
    post = get_object_or_404(BlogPost, id=post_id)
    entries = post.entry_set.order_by('-date_added')
    if post.owner != request.user:
        raise Http404
    context = {'post': post, 'entries': entries}
    return render(request, 'blogs/post.html', context)
@login_required    
def new_post(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user  
            new_post.save()
            return redirect('blogs:posts')
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)
@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись Entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    blog_post = entry.topic  
    if post.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=blog_post.id)

    context = {'entry': entry, 'blog_post': blog_post, 'form': form}
    return render(request, 'blogs/edit_entry.html', context)
@login_required
def edit_post(request, post_id):
    """Редактирует существующий блог-пост."""
    post = get_object_or_404(BlogPost, id=post_id)

    if post.owner != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот пост.")

    if request.method != 'POST':
        form = BlogForm(instance=post)
    else:
        form = BlogForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)

    context = {'form': form, 'post': post}
    return render(request, 'blogs/edit_post.html', context)
@login_required
def new_entry(request, post_id):
    """Добавляет новую запись к посту."""
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = post
            new_entry.save()
            return redirect('blogs:post', post_id=post.id)

    context = {'form': form, 'post': post}
    return render(request, 'blogs/new_entry.html', context)
@login_required
def register(request):
    """Регистрирует нового пользователя."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('blogs:index')  # Перенаправление на главную страницу блога

    context = {'form': form}
    return render(request, 'registration/register.html', context)

    
