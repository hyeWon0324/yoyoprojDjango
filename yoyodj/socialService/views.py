from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Posts, Comments, Tracks, Users, Likes, Friends
from .social_models import TrackPost
from .forms import PostForm, TrackForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def list_posts(request):
    try:
        qs = Posts.objects.all()
        qs = qs.filter(created_dt__lte=datetime.utcnow())
        posts = qs.order_by('-created_dt')
        #posts = qs.order_by('-id')
        track_posts = []
        for post in posts:
            '''
            track = post.track_idx
            track_post = TrackPost(title=track.title, track_type=track.type_idx,
                                   played_count=track.played_count, moods=track.moods, genre=track.genre_idx,
                                   track_source=track.track_source, image=track.image,
                                   tags=post.tags, contents=post.contents, comment_count=post.comments_count,
                                   likes_count=post.likes_count, follower_count=post.follower_count,
                                   created_dt=post.created_dt, updated_dt=post.updated_dt)
            '''
            track_post = TrackPost(track=post.track_idx, post=post, user=post.users_idx)
            track_posts.append(track_post)

        return render(request, 'socialService/list_posts.html',
                  {'track_posts': track_posts})
    except ObjectDoesNotExist:
        print("Either the entry or track doesn't exist.")


def post_detail(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    track_post = TrackPost(track=post.track_idx, post=post, user=post.users_idx)
    track_post.setComment()
    form = CommentForm()
    #post = Posts.objects.get(idx=pk)
    return render(request, 'socialService/post_detail.html', {'post': track_post, 'form': form})


def post_new(request):
    # request.POST, request.FILES

    if request.method == "POST":
        #args = {"form1" = PostForm(request.POST, request.FILES)}
        form = PostForm(request.POST, request.FILES)
        form2 = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            #post.users_idx = request.user
            #post.track_idx = request.track_idx
            post.created_dt = datetime.utcnow()
            post.updated_dt = post.created_dt

            track = form2.save(commit=False)

            track.save()

            post.save()

        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        form2 = TrackForm()
    return render(request, 'socialService/post_edit.html', {'form': form, 'form2': form2})


def post_edit(request, pk, pk2):
    user = get_object_or_404(Users, pk=pk)
    post = get_object_or_404(Posts, pk=pk2)
    track = post.track_idx
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        form2 = TrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            post = form.save(commit=False)
            post.users_idx = user
            post.created_dt = datetime.utcnow()
            post.updated_dt = datetime.utcnow()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        form2 = TrackForm(instance=track)
    return render(request, 'socialService/post_edit.html', {'form': form, 'form2': form2})


def post_remove(request, pk):
    post = get_object_or_404(Posts, pk=pk)

    if request.user.is_authenticated():
        post.delete()
        return redirect('list_posts')

    return redirect('post_detail', pk=post.pk)


def already_liked_post(user, post_id):

    post = Posts.objects.get(pk=post_id)
    return Likes.objects.filter(users_idx=user, posts_idx=post).exists()


def like_post(request, post_id):

    if request.user.is_authenticated():
        post = Posts.objects.get(id=post_id)

        if already_liked_post(request.user, post_id):
            Likes.objects.filter(users_idx=request.user, posts_idx=post).delete()
        else:
            Likes.objects.create(users_idx=request.user, posts_idx=post, created_dt=datetime.now())

        return redirect(reverse('index'))
    else:
        return redirect(reverse('list_posts'))


def add_comment_to_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posts_idx = post
            #comment.users_idx = request.user
            comment.users_idx = post.users_idx
            comment.save()

            post.comments_count += 1
            post.save()

    return redirect('post_detail', pk=post.pk)


def comment_remove(request, post_id, comment_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.comments_count -= 1
    post.save()

    comment = get_object_or_404(Comments, pk=comment_id)
    comment.delete()

    return redirect('post_detail', pk=comment.posts_idx.pk)


def get_profile_avatar():
    pass

def get_user_badge():
    followers = 0
    track_count = 0
    username =''
    avatar = ''





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