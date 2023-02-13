from django.shortcuts import render
from posts.models import Post
from profiles.models import Profile
from django.db.models import Q

# Create your views here.


def search_posts_view(request) :
    template_name = "search/search.html"
    q = request.GET.get("q")
    posts = Post.objects.search(q)
    profile = Profile.objects.search(q)
    context = {
        "posts":posts,
        "profile":profile
     }
    return render(request, template_name, context)