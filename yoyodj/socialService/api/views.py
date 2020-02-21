from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
import jwt
from rest_framework.response import Response

from ..models import Posts, Friends, Users, Comments, Likes
from .serializers import PostModelSerializer


class LikeToggleAPIView(APIView):
    pass


class PostCreateAPIView(generics.CreateAPIView):

    serializer_class = PostModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        #request body 에 있는 track-idx 받는다
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
    serializer_class = PostModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs.get("pk")
        qs = Posts.objects.filter(pk=post_id)
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(select={"": ''})
        return qs.order_by('-created_dt')


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostModelSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(PostListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get("idx")

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
    success_url = reverse_lazy("post:list") #reverse()