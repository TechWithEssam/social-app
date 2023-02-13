from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Post, LikePost, Comment, LikeComment
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, AddCommentForm
# Create your views here.

@login_required
def home_view(request) :
    template_name = "posts/home.html"
    profile = Profile.objects.get(user=request.user)
    post = profile.get_my_posts_and_my_friends_posts()
    is_empty = False
    if len(post) == 0 :
        is_empty = True
    context = {
        "post":post[:10],
        "is_empty":is_empty,
        "profile":profile
    }
    return render(request, template_name, context)

@login_required
def like_unlike_posts_view(request) :
    if request.method == "POST" :
        post_pk = request.POST.get("post_pk")
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(user=request.user)
        if profile in post.liked.all() :
            post.liked.remove(profile)
        else :
            post.liked.add(profile)
    like, created = LikePost.objects.get_or_create(
        user = profile,
        post = post,
    )
    if not created :
        if like.value == "Like" :
            like.value = "UnLike"
        else :
            like.value = "Like"
    else :
        like.value = "Like"
    like.save()
    post.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def create_post_view(request) :
    template_name = "posts/create_update.html"
    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid() :
        instance = form.save(commit=False)
        instance.auther = Profile.objects.get(user=request.user)
        instance.save()
        return redirect(instance.get_detail_post_url())
    context = {"c_form":form}
    return render(request, template_name, context)

@login_required
def update_post_view(request, slug) :
    template_name = "posts/create_update.html"
    post = Post.objects.get(slug=slug)
    form = CreatePostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid() :
        form.save()
        return redirect(post.get_detail_post_url())
    context = {"u_form":form}
    return render(request, template_name, context)

@login_required
def delete_post_view(request, slug) :
    template_name = "posts/create_update.html"
    post = Post.objects.get(slug=slug)
    if request.method == "POST" :
        post.delete()
        return redirect("/")
    context={"post":post}
    return render(request, template_name, context)

@login_required
def detail_post_and_add_comment(request, slug) :
    profile = Profile.objects.get(user=request.user)
    template_name = "posts/detail_post_comment.html"
    try :
        qs = Post.objects.get(slug=slug)
        form = AddCommentForm(request.POST or None)
        if form.is_valid() :
            instance = form.save(commit=False)
            instance.post = qs
            instance.user = profile
            instance.save()
            return redirect(qs.get_detail_post_url())
    except :
        return HttpResponse("<h2>your request not fount pleace chack your link......</h2>")
    is_empty = False
    comments = qs.get_all_comment()
    if len(comments) == 0 :
        is_empty = True
    context = {
        "qs" : qs,
        "form":form,
        "comments":comments,
        "is_empty" : is_empty,
        "profile":profile
    }
    return render(request, template_name, context)

@login_required
def like_unlike_commet_view(request) :
    if request.method == "POST" :
        comment_pk = request.POST.get("comment_pk")
        comment = Comment.objects.get(pk=comment_pk)
        profile = Profile.objects.get(user=request.user)
        if profile in comment.like.all() :
            comment.like.remove(profile)
        else :
            comment.like.add(profile)

    like, created = LikeComment.objects.get_or_create(comment = comment,user = profile)
    if not created :
        if like.value == "Like" :
            like.value = "UnLike"
        else :
            like.value = "Like"
    else :
        like.value = "Like"
    like.save()
    comment.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def update_comment_view(request, slug) :
    template_name = "posts/create_update.html"
    qs = Comment.objects.get(slug=slug)
    form = AddCommentForm(request.POST or None, instance=qs)
    if form.is_valid() :
        form.save()
        return redirect(qs.post.get_detail_post_url())
    context = {"update_comment":form}
    return render(request, template_name, context)

@login_required
def delete_comment_view(request, slug) :
    qs = Comment.objects.get(slug=slug)
    qs.delete()
    return redirect(request.META.get('HTTP_REFERER'))