from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, ProfileForm, RegisterForm, CommentForm
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Comment, Like, Profile

def home(request):

    posts = Post.objects.all().order_by("-created_at")

    paginator = Paginator(posts, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/home.html",
        {
            "page_obj": page_obj
        }
    )

def post_detail(request, id):

    post = get_object_or_404(Post, id=id)

    user_liked = False

    if request.user.is_authenticated:

        user_liked = Like.objects.filter(
            post=post,
            user=request.user
        ).exists()

    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "user_liked": user_liked,
            "comment_form": comment_form,
        }
    )

@login_required
def add_comment(request, id):

    post = get_object_or_404(Post, id=id)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post

            comment.author = request.user

            comment.save()

    return redirect(
        "post_detail",
        id=post.id
    )

@login_required
def create_post(request):

    if request.method == "POST":

        form = CreatePostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()

            return redirect("post_detail", id=post.id)

    else:

        form = CreatePostForm()

    return render(
        request,
        "blog/create_post.html",
        {
            "form": form
        }
    )

@login_required
def edit_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden(
            "You are not allowed to edit this post."
        )

    if request.method == "POST":

        form = CreatePostForm(
            request.POST,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect(
                "post_detail",
                id=post.id
            )

    else:

        form = CreatePostForm(
            instance=post
        )

    return render(
        request,
        "blog/edit_post.html",
        {
            "form": form,
            "post": post
        }
    )

@login_required
def delete_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden(
            "You are not allowed to delete this post."
        )

    if request.method == "POST":

        post.delete()

        return redirect("home")

    return render(
        request,
        "blog/delete_post.html",
        {
            "post": post
        }
    )

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "blog/register.html",
        {
            "form": form
        }
    )

def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                next_url = request.POST.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("home")

    else:

        form = AuthenticationForm()

    next_url = request.GET.get("next", "")

    return render(
        request,
        "blog/login.html",
        {
            "form": form,
            "next": next_url,
        }
    )

@login_required
def user_logout(request):

    if request.method == "POST":
        logout(request)

    return redirect("home")

@login_required
def dashboard(request):

    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")

    total_posts = posts.count()

    total_likes = Like.objects.filter(
        post__author=request.user
    ).count()

    total_comments = Comment.objects.filter(
        post__author=request.user
    ).count()

    return render(
        request,
        "blog/dashboard.html",
        {
            "posts": posts,
            "total_posts": total_posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
        }
    )
@login_required
def like_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.method == "POST":

        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            like.delete()

    return redirect(
        "post_detail",
        id=post.id
    )

def about(request):
    return render(
        request,
        "blog/about.html"
    )

@login_required
def profile(request):

    user = request.user

    posts = Post.objects.filter(
        author=user
    ).order_by("-created_at")

    total_posts = posts.count()

    total_likes = Like.objects.filter(
        post__author=user
    ).count()

    total_comments = Comment.objects.filter(
        author=user
    ).count()

    return render(
        request,
        "blog/profile.html",
        {
            "profile_user": user,
            "posts": posts,
            "total_posts": total_posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
        }
    )

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "blog/edit_profile.html",
        {
            "form": form
        }
    )

def search(request):

    query = request.GET.get("q", "").strip()

    posts = Post.objects.none()

    if query:

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).select_related(
            "author"
        ).order_by(
            "-created_at"
        )

    paginator = Paginator(posts, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/search.html",
        {
            "query": query,
            "posts": posts,
            "page_obj": page_obj,
        }
    )