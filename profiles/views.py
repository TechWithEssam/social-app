from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from .models import Profile, RelationshipFriends
from .forms import RegisterForm, AuthenticationUserForm, ProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse


def register_form_view(request) :
    template_name = "profiles/authentication.html"
    form = RegisterForm(request.POST or None)
    if form.is_valid() :
        user = form.save(commit=False)
        user.save()
        login(request, user)
        return redirect("/")
    context = {"register_form":form}
    return render(request, template_name, context)

def authentication_form_view(request) :
    template_name = "profiles/authentication.html"
    form = AuthenticationUserForm(request.POST, data=request.POST or None)
    if form.is_valid() :
        user = form.get_user()
        login(request, user)
        return redirect("/")
    context = {"auth_form":form}
    return render(request, template_name, context)

def logout_user_view(request) :
    logout(request)
    return redirect("profiles:login")

@login_required
def my_profile_view(request) :
    template_name = "profiles/my_profile.html"
    profile = Profile.objects.get(user=request.user)
    context = {"profile":profile,}
    return render(request, template_name, context)

@login_required
def get_profile_user_view(request, slug) :
    template_name = "profiles/user_profile.html"
    try :
        profile = Profile.objects.get(slug=slug)
        me = Profile.objects.get(user=request.user)
        relation_r = RelationshipFriends.objects.filter(sender=me)
        relation_s = RelationshipFriends.objects.filter(receiver=me)
        relation_sender = set()
        relation_receiver = set()
        for item in relation_r :
            relation_receiver.add(item.receiver.user)
        for item in relation_s :
            relation_sender.add(item.sender.user)
    except :
        return HttpResponse("<h1>you request not fount please check and try again thanks</h1>")
    context = {
        "profile":profile,
        "relation_sender":relation_sender,
        "relation_receiver" :relation_receiver
    }
    return render(request, template_name, context)


@login_required
def invatation_friends_view(request) :
    template_name = "profiles/invatation_friends.html"
    obj = Profile.objects.get_profile_to_sender_invite(request.user)
    profile = Profile.objects.get(user=request.user)
    qs = RelationshipFriends.objects.invatations_received(profile)
    relation_r = RelationshipFriends.objects.filter(sender=profile)
    relation_s = RelationshipFriends.objects.filter(receiver=profile)
    relation_sender = set()
    relation_receiver = set()
    for item in relation_s :
        relation_sender.add(item.sender.user)
    for item in relation_r :
        relation_receiver.add(item.receiver.user)
    result = list(map(lambda x :x.sender, qs))
    is_empty = False
    if len(qs) == 0 :
        is_empty = True
    context = {
                 "qs":result,
                 "is_empty": is_empty,
                 "obj" :obj,
                 "relation_sender":relation_sender,
                 "relation_receiver":relation_receiver
        }
    return render(request, template_name, context)

@login_required
def accept_invite_view(request) :
    if request.method == "POST" :
        profile_pk = request.POST.get("profile_pk")
        sender =Profile.objects.get(pk=profile_pk)
        receiver = Profile.objects.get(user=request.user)
        rel = RelationshipFriends.objects.get(sender=sender, receiver=receiver)
        if rel.status == "send" :
            rel.status = "accepted"
            rel.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def reject_invite_view(request) :
    if request.method == "POST" :
        profile_pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk=profile_pk)
        receiver = Profile.objects.get(user=request.user)
        rel = RelationshipFriends.objects.get(sender=sender, receiver=receiver)
        rel.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def send_invite_view(request) :
    if request.method == "POST" :
        profile_pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=profile_pk)
        rel = RelationshipFriends.objects.create(
            sender=sender,
            receiver=receiver,
            status = "send"
        )
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_profile_from_friends_view(request) :
    if request.method == "POST" :
        profile_pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=profile_pk)
        relation = RelationshipFriends.objects.get((Q(sender=sender)& Q(receiver=receiver)) |(Q(sender=receiver) & Q(receiver=sender)))
        relation.delete()
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
def update_profile_info_view(request) :
    template_name = "profiles/update_profile.html"
    user = request.user
    profile = Profile.objects.get(user=user)
    user_form = UserForm(request.POST or None, instance=user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid() and user_form.is_valid():
        user_form.save()
        form.save()
        return redirect(profile.get_my_profile())
    context = {"profile_form":form, "user_form":user_form}
    return render(request, template_name, context)

