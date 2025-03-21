from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Response, Category
from .forms import PostForm, ResponseForm, NewsletterForm
from django.contrib import messages


def home(request):
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(category_id=category_id)
    else:
        posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)

    # Получаем номер текущей страницы из запроса
    page_number = request.GET.get('page')

    # Получаем объект страницы
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'board/home.html',
                  {'posts': posts,
                   'page_obj': page_obj,
                   'categories': categories})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    responses = Response.objects.filter(post=post)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ResponseForm()
    return render(request, 'board/post_detail.html', {'post': post, 'responses': responses, 'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'board/post_create.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Проверяем, является ли текущий пользователь автором объявления
    if request.user != post.author:
        messages.error(request, "Вы не можете редактировать это объявление, так как вы не его автор.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Объявление успешно обновлено.")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'board/post_edit.html', {'form': form, 'post': post})


@login_required
def response_accept(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.accepted = True
    response.save()
    return redirect('post_detail', pk=response.post.pk)


@login_required
def response_delete(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.delete()
    return redirect('post_detail', pk=response.post.pk)


@login_required
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save()
            newsletter.send_emails()  # Отправляем рассылку
            return redirect('home')
    else:
        form = NewsletterForm()
    return render(request, 'board/create_newsletter.html', {'form': form})
