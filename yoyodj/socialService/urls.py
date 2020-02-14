from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_posts, name='list_posts'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('upload/', views.post_new, name='post_new'),
    path('post/<int:pk>/<int:pk2>/edit', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:post_id>/comment/<int:comment_id>/remove', views.comment_remove, name='comment_remove'),
]

#url(r'^profile/<int:id>', views.list_posts, name='post-stream'),
#url(r'^upload/<int:id>', views.add_post, name='post-upload'),
#url(r'^comment/<int:id>', views.add_comment, name='post-comment')
#path('post/<int:pk>/<int:pk2>/edit', views.post_edit, name='post_edit'),

#path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
#path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),