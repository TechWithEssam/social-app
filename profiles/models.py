from django.urls import reverse
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from .utils import slugify_instance_user
import random
from django.db.models import Q
from itertools import chain

GENDER = (
    ("Male","Male"),
    ("Female", "Female")
)

class ProfileManager(models.Manager) :
    def search(self, query=None) :
        if query is None or query == "" :
            return self.none()
        lookup = Q(user__username__icontains=query) or Q(user__first_name__icontains=query)
        return self.filter(lookup)
    def get_profile_to_sender_invite(self, sender) :
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = RelationshipFriends.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = set()
        for item in qs :
            if item.status == "accepted" :
                accepted.add(item.sender)
                accepted.add(item.receiver)
        available = [_ for _ in profiles if _ not in accepted]
        random.shuffle(available)
        return available[:6]
class PostManager(models.Manager) :
    def get_queryset(self) :
        return ProfileManager(self.model, using=self._db)
    def search(self, query) :
        return self.get_queryset().search(query=query)
class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', default="avatars/no_avatar.png")
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    gender = models.CharField(choices=GENDER, max_length=6, blank=True)
    country = models.CharField(max_length=122, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ProfileManager()
    def __str__(self) :
        return self.user.username
    
    def get_profile_user(self) :
        return reverse("profiles:profile_user",kwargs={"slug":self.slug})
    
    def get_my_profile(self) :
        return reverse("profiles:my_profile")
    
    def get_url_update_info_profile(self) :
        return reverse("profiles:update_info")
        
    def get_avatar_url(self) :
        try :
            url = self.avatar.url
        except :
            url = None
        return url
    
    def get_all_friends(self) :
         return self.friends.all()
    
    def get_num_of_friends(self) :
        return self.get_all_friends().count()
    
    def get_all_posts(self) :
        return self.post_set.all()
    
    def get_num_of_posts(self) :
        return self.get_all_posts().count()

    def get_my_posts_and_my_friends_posts(self) :
        users = [user for user in self.get_all_friends()]
        posts = set()
        qs = None 
        for user in users :
            profile = Profile.objects.get(user=user)
            post_profile = profile.post_set.all()
            posts.add(post_profile)
        my_posts = self.post_set.all()
        posts.add(my_posts)
        if len(posts) > 0 :
           qs =  sorted(chain(*posts),reverse=True, key=lambda x:x.created)
        random.shuffle(qs)
        return qs[:10]
    
    






STATUS_CHOICES = (
    ("send","send"),
    ("accepted","accepted")
)

class RelationshipManager(models.Manager) :
    def invatations_received(self, receiver) :
        qs = RelationshipFriends.objects.filter(receiver=receiver, status="send")
        return qs

class RelationshipFriends(models.Model) :
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = RelationshipManager()

    def __str__(self) :
        return f"{self.sender.user}-{self.receiver.user}-{self.status}"
    


def post_save_slug_profile(sender, instance, created, **kwargs) :
    if created :
        slugify_instance_user(instance, save=True)
post_save.connect(post_save_slug_profile, sender=Profile)