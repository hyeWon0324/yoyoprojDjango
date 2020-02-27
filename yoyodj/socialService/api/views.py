from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions, reverse
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
import jwt
from rest_framework.response import Response

from ..models import Posts, Friends, Users, Comments, Likes
from .serializers import TrackPostModelSerializer, UserProfileDisplaySerializer

# api/post/:post_id/like/
# api/post/:post_id/unlike/

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, format=None):
        user = Users.objects.get(user_id=user_id)
        post_qs = Posts.objects.filter(users_idx=user.idx)
        message = "Auth error "

        access_token = self.request.data.get("access_token")

        if access_token is not None:
            payload = jwt.decode(access_token, 'HS256')
            user_idx = payload['idx']  # user_id, idx, email
            user = Users.objects.get(user_idx=user_idx)
            #self.request.user = user
            is_liked = Posts.objects.like_toggle(user, post_qs.first())
            return Response({'liked': is_liked})
        return Response({"message": message}, status=203)


# api / profile / feeds / < str: users_id >

class UserProfileAPIView(APIView):
    serializer_class = UserProfileDisplaySerializer

    def get(self, request, user_id):
        access_token = self.request.data.get("access_token")

        if access_token is not None:
            payload = jwt.decode(access_token, 'HS256')
            user_idx = payload['idx']  # user_id, idx, email
            user = Users.objects.get(user_idx=user_idx)
            #self.request.user = user


# api / follow /: my_id /:user_id
#
# api/unfollow/:my_id/:user_id
#
class FollowToggleAPIView(APIView):

    def get(self, request, username, *args, **kwargs):
        access_token = self.request.data.get("access_token")

        if access_token is not None:
            payload = jwt.decode(access_token, 'HS256')
            user_idx = payload['idx']  # user_id, idx, email
            user = Users.objects.get(user_idx=user_idx)

            is_following = Users.objects.toggle_follow(user, )
        return reverse("profiles:detail", username=username)
        # url = reverse("profiles:detail", kwargs={"username": username})
        # HttpResponseRedirect(url)



# api/profile/mr/<str:users_id>


# api/profile/song/<str:users_id>


# api/profile/following/<str: sender_id>
#
# api/profile/followers/<str:receiver_id>
#
# api / profile / likes /: user_id
#
# messages/:my_id/:user_id
#
# api / post /: user_id /:post_id
#
# api/upload/post/
#
# post/user_id/post_idx/edit
#
# api/post/user_id/post_idx/remove
#
# api/post/<string:user_id>/<int:post_id>/comment/
#




class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = TrackPostModelSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # request body 에 있는 track-idx 받는다
        access_token = self.request.data.get("access_token")

        if access_token is not None:
            payload = jwt.decode(access_token, 'HS256')
            user_idx = payload['idx']  # user_id, idx, email
            user = Users.objects.get(user_idx=user_idx)
            self.request.user = user
        serializer.save(user=self.request.user)
        response = self.get_response(self.request)

        return response


class PostDetailAPIView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = TrackPostModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        qs = Posts.objects.filter(pk=post_id)
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(select={"": ''})
        return qs.order_by('-created_dt')


class PostListAPIView(generics.ListAPIView):
    serializer_class = TrackPostModelSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(PostListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get("user_id")

        if requested_user:
            qs = Posts.objects.filter(users_idx__idx=requested_user).order_by("-created_dt")
        else:
            im_following = Friends.objects.get_following(requested_user)  # none
            qs1 = Posts.objects.filter(users_idx__in=im_following)
            qs2 = Posts.objects.filter(users_idx=self.request.user)
            qs = (qs1 | qs2).distinct().order_by("-created_dt")

        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(contents__icontains=query) |
                Q(users_idx__nickname__icontains=query)
            )
        return qs


class TweetDeleteView(APIView):
    model = Posts
    template_name = 'posts/delete_confirm.html'
    success_url = reverse_lazy("post:list")  # reverse()
