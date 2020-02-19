from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from ..models import Posts
from .serializers import PostModelSerializer


class TweetDetailAPIView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        tweet_id = self.kwargs.get("pk")
        qs = Posts.objects.filter(pk=tweet_id)
        if qs.exists() and qs.count() == 1:
            parent_obj = qs.first()
            qs1 = parent_obj.get_children()
            qs = (qs | qs1).distinct().extra(select={"parent_id_null": 'parent_id IS NULL'})
        return qs.order_by("-parent_id_null", '-created_dt')


class TweetListAPIView(generics.ListAPIView):
    serializer_class = PostModelSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(TweetListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        requested_user = self.kwargs.get("idx")

        if requested_user:
            qs = Posts.objects.filter(user_idx__idx=requested_user).order_by("-created_dt")
        else:
            im_following = self.request.user.profile.get_following()  # none
            qs1 = Posts.objects.filter(users_idx__in=im_following)
            qs2 = Posts.objects.filter(user=self.request.user)
            qs = (qs1 | qs2).distinct().order_by("-created_dt")

        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(contents__icontains=query) |
                Q(user_idx__nickname__icontains=query)
            )
        return qs