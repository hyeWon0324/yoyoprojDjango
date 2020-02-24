from django.urls import path
from . import views
from .views import (
    LikeToggleAPIView,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,

    )

urlpatterns = [
    path('feeds/<int:user_id>/', PostListAPIView.as_view(), name='list'),  # /api/profile/
    path('mr/<int:user_id>/'),
    path('song/<int:user_id>/'),
    path('following/<int:user_id>/'),
    path('followers/<int:user_id>/'),
    path('likes/<int:user_id>/'),
]