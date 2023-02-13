from django.urls import path
from .views import search_posts_view

app_name="search"
urlpatterns = [ 
    path("search/", search_posts_view, name="search")
]