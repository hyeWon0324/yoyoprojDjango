from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_posts, name='list_posts'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('upload/', views.post_new, name='post_new'),
]

#url(r'^profile/<int:id>', views.list_posts, name='post-stream'),
#url(r'^upload/<int:id>', views.add_post, name='post-upload'),
#url(r'^comment/<int:id>', views.add_comment, name='post-comment')