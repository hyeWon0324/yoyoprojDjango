from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import PostForm
from .models import Posts, Comments, Users
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.

# @login_required(login_url = "user:login")

def add_post(request):
    # upload a post
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            track_post = form.save(commit=False)

            track_post.generate()
            messages.success(request, "post uploaded successfully")
            return redirect('profile.html')
    else:
        form = PostForm()
        return render(request, 'upload_form.html', {'form': form})


def list_posts(request):
    # get a list of posts in the profile page

    keyword = request.GET.get("keyword")

    if keyword:
        posts = Posts.objects.filter(title__contains=keyword)
        return render(request, "track_post_list.html", {"posts": posts})
    posts = Posts.objects.all()

    return render(request, "posts.html", {"posts": posts})


def detail_post(request, id):
    # article = Article.objects.filter(id = id).first()
    post = get_object_or_404(Posts, id=id)

    comments = post.comments.all()
    return render(request, "detail.html", {"post": post, "comments": comments})


#@login_required(login_url="user:login")
def update_post(request, id):
    post = get_object_or_404(Posts, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        article = form.save(commit=False)

        article.author = request.user
        article.save()

        messages.success(request, "Post successfully updated")
        return redirect("")

    return render(request, "profile.html", {"form": form})


@login_required(login_url="user:login")
def delete_post(request, idx):
    post = get_object_or_404(Posts, id=idx)

    post.delete()

    messages.success(request, "Post successfully Deleted")

    return redirect("")


def add_comment(request, idx):
    post = get_object_or_404(Posts, id=idx)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        new_comment = Comments(comment_author=comment_author, comment_content=comment_content)

        new_comment.posts_idx = post

        new_comment.save()
    return redirect(reverse("post:detail", kwargs={"id": idx}))
