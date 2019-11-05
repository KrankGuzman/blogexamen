from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import models as auth_models
from django.shortcuts import redirect, render

from . import forms as app_forms
from . import models as app_models
from . import queries as app_queries


# VIEWS: ACCOUNT #
def home(request):
    return render(request, 'Account/Home.html', {})


def log_in_view(request):
    if request.method == 'POST':
        log_in_form = app_forms.LogInForm(request.POST)
        if log_in_form.is_valid():
            username = log_in_form.cleaned_data.get("username")
            password = log_in_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'App/LogIn.html', {'form': log_in_form})
            login(request, user)
            return redirect(home)
    else:
        log_in_form = app_forms.LogInForm()
    return render(request, 'Account/LogIn.html', {'log_in_form': log_in_form})


def log_out_view(request):
    logout(request)
    return redirect(home)


def sign_in_view(request):
    if request.method == 'POST':
        sign_in_form = app_forms.SignInForm(request.POST)
        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data.get("username")
            first_name = sign_in_form.cleaned_data.get("first_name")
            last_name = sign_in_form.cleaned_data.get("last_name")
            email = sign_in_form.cleaned_data.get("email")
            password = sign_in_form.cleaned_data.get("password")

            new_user = auth_models.User(username=username, first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return redirect(home)
    else:
        sign_in_form = app_forms.SignInForm()
    return render(request, 'Account/SignIn.html', {'sign_in_form': sign_in_form})


# VIEWS: POST #
def post_index_view(request):
    posts = app_models.Post.objects.all().order_by('title')
    records = app_models.PostRecord.objects.filter(action='CREATE').order_by('post')
    return render(request, 'App/PostIndex.html', {'posts': posts, 'records': records})


def create_post_view(request):
    user = request.user
    form = app_forms.PostForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():

            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            status = form.cleaned_data['status']
            tags = request.POST.getlist('tags')

            new_post = app_models.Post()
            new_post.title = title
            new_post.text = text
            new_post.status = status
            new_post.save()

            new_post_record = app_models.PostRecord()
            new_post_record.post = new_post
            new_post_record.user = user
            new_post_record.action = "CREATE"
            new_post_record.save()

            for tag in tags:
                new_tag = app_models.Tag.objects.get(pk=tag)
                new_tag_of_post = app_models.TagOfPost()
                new_tag_of_post.post = new_post
                new_tag_of_post.tag = new_tag
                new_tag_of_post.save()

            return post_index_view(request)
    return render(request, 'App/CreatePost.html', {'post_form': app_forms.PostForm()})


def read_post_view(request, post_pk):
    # Get: User from the request #
    user = request.user

    # Query: get post by id#
    post = app_models.Post.objects.get(id=post_pk)
    post.record_create = app_models.PostRecord.objects.get(post=post, action='CREATE')
    post.comments = app_models.PostComment.objects.filter(post=post)
    for post_comment in post.comments:
        post_comment.record_create = app_models.PostCommentRecord.objects.get(post_comment=post_comment, action='CREATE')

    post_comment_form = app_forms.PostCommentForm()
    if request.method == 'POST':
        # Get: Form from the request #
        post_comment_form = app_forms.PostCommentForm(request.POST)
        if post_comment_form.is_valid():

            # Create: new post comment #
            new_post_comment = app_models.PostComment()
            new_post_comment.post = app_models.Post.objects.get(id=post_pk)
            new_post_comment.text = post_comment_form.cleaned_data['text']

            # Save: new post comment #
            new_post_comment.save()

            # Create: new post comment record #
            new_post_comment_record = app_models.PostCommentRecord()
            new_post_comment_record.post_comment = new_post_comment
            new_post_comment_record.user = user
            new_post_comment_record.action = "CREATE"

            # Save: new post comment record #
            new_post_comment_record.save()

            # Reset: form #
            request.POST = app_forms.PostCommentForm()
            return redirect(read_post_view, post_pk)
    return render(request, 'App/ReadPost.html', {
            'post': post,
            'post_comment_form': post_comment_form
        })


def delete_post(request, post_pk):
    post = app_queries.get_post_by_pk(post_pk)


def post_comment_index_view(request, post_pk):
    post = app_queries.get_post_by_pk(post_pk)


def delete_post_comment_view(request, post_comment_pk):
    user = request.user
    post_comment = app_models.PostComment.objects.get(id=post_comment_pk)
    post = post_comment.post
    if post_comment:
        post_comment_record = app_models.PostCommentRecord.objects.get(post_comment=post_comment, action='CREATE')
        if post_comment_record.user == user:
            post_comment.delete()
            return redirect(read_post_view, post.pk)
    print('Nothing')
