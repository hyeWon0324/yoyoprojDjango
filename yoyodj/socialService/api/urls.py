from django.urls import path
from . import views
from .views import (
    LikeToggleAPIView,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,

    )

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),  # /api/tweet/
]