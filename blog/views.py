from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializer import PostSerializer
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from drf_yasg.utils import swagger_auto_schema




# class PostListCreateAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     @swagger_auto_schema(request_body=PostSerializer)
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     @swagger_auto_schema(request_body=PostSerializer)
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def post_list(request):
    tag_name = request.GET.get("tag")
    posts = Post.objects.all().order_by('-created_at')

    if tag_name:
        posts = posts.filter(tags__name=tag_name)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'post_list.html', {"posts": posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'post_detail.html', {"post": post})


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

    return render(request, 'post_form.html', {"form": form})


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

    return render(request, 'post_form.html', {"form": form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    post.delete()
    return redirect('post_list')


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect("blogs:post_list")
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blogs:post_list")
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("blogs:logout")