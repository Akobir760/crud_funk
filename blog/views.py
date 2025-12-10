from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Tag
from .forms import PostForm
from django.core.paginator import Paginator


def post_list(request):
    tag_name = request.GET.get("tag")
    posts = Post.objects.all().order_by('-created_at')

    if tag_name:
        posts = posts.filter(tags__name=tag_name)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'templates/post_list.html', {"posts": posts})



def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'templates/post_detail.html', {"post": post})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'templates/post_form.html', {"form": form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'templates/post_form.html', {"form": form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    post.delete()
    return redirect('post_list')