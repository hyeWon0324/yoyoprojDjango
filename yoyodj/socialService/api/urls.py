from django.urls import path
from . import views
from .views import (
    LikeToggleAPIView,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,

    )

urlpatterns = [
    path('feeds/<string:user_id>/', PostListAPIView.as_view(), name='list'),  # /api/profile/
    path('mr/<string:user_id>/'),
    path('song/<string:user_id>/'),
    path('following/<string:user_id>/'),
    path('followers/<string:user_id>/'),
    path('likes/<string:user_id>/'),
]