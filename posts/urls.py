from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [ 
    path('', views.home_view, name="home"),
    path('like-unlike/', views.like_unlike_posts_view, name="like_unlike"),
    path("create/", views.create_post_view, name="create_post"),
    path("update-post/<slug>/", views.update_post_view, name="update_post"),
    path("delee-post/<slug>/", views.delete_post_view, name="delete_post"),
    path("deltail-post/<slug>/", views.detail_post_and_add_comment, name="detail_post"),
    path("like-unlike-comment/", views.like_unlike_commet_view, name="like_unlike_comment"),
    path("update-comment/<slug>/", views.update_comment_view, name="update_comment"),
    path("delete-comment/<slug>/", views.delete_comment_view, name="delete_comment")
]
