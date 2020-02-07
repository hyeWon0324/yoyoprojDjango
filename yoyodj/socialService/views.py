from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Posts, Comments, Tracks, Users
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

class TrackPost:
    # track info
    title = ''
    track_type = 0
    played_count = 0
    moods = ''       # mood tags if MR
    genre = ''       # genre if song
    track_source =''
    image = ''

    # post info
    tags = []        # additional tags by author
    desc = ''

    # user info
    author_name = ''
    follower_count = 0
    track_count = 0

    def __init__(self, title, track_type, played_count, moods, follower, contents):
        self.follower_count = follower
        self.desc = contents


def list_posts(request):
    try:
        qs = Posts.objects.all()
        qs = qs.filter(created_dt__lte=datetime.now())
        posts = qs.order_by('-created_dt')
        #posts = qs.order_by('-id')
        tracks = []
        for post in posts:
            tracks.append(Tracks.objects.get(idx=post.track_idx))
        track_posts = TrackPost()
        return render(request, 'socialService/list_posts.html',
                  {'track_posts': track_posts})
    except ObjectDoesNotExist:
        print("Either the entry or track doesn't exist.")

# Create your views here.
'''
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

    return render(request, "page.html", {"posts": posts})


def detail_post(request, id):
    # article = Article.objects.filter(id = id).first()
    post = get_object_or_404(Posts, id=id)

    comments = post.comments.all()
    return render(request, "page.html", {"post": post, "comments": comments})


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
'''