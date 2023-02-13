from django.db.models import Q
from django.db import models
from profiles.models import Profile
from django.urls import reverse
from .utils import slugify_url_post, make_slug_url_comment
# Create your models here.


VALUE_CHOICES = (
    ("Like","Like"),
    ("UnLike", "UnLike")
)


class PostQuerySet(models.QuerySet) :
    def search(self, query=None) :
        if query is None or query == "" :
            return self.none()
        lookup = Q(text__icontains=query)
        return self.filter(lookup)
class PostManager(models.Manager) :
    def get_queryset(self) :
        return PostQuerySet(self.model, using=self._db)
    def search(self, query) :
        return self.get_queryset().search(query=query)

class Post(models.Model) :
    auther = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to="posts", blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = PostManager()
    
    def __str__(self) :
        return f"{self.text[:50]}-- {self.auther}-- {self.created.strftime('%d_%m_%y')}"
    

    def get_all_user_liked(self) :
        return self.liked.all()
    
    def get_all_no_of_like(self) :
        return self.get_all_user_liked().count()
        
    def save(self, *args, **kwargs) :
        if not self.slug :
            self.slug = slugify_url_post()
        return super().save(*args, **kwargs)
    
    def get_all_comment(self) :
        return self.comment_set.all()
    
    def get_all_comment_num(self) :
        return self.get_all_comment().count()
    
    def get_detail_post_url(self) :
        return reverse("posts:detail_post", kwargs={"slug":self.slug})

    def get_url_update_post(self) :
        return reverse("posts:update_post", kwargs={"slug":self.slug})
    
    def get_url_delete_post(self) :
        return reverse("posts:delete_post", kwargs={"slug":self.slug})

class LikePost(models.Model) :
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=6, choices=VALUE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self) :
        return f"{self.post}-{self.user}-{self.value}"


class Comment(models.Model) :
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=1500)
    slug = models.SlugField(blank=True, null=True, unique=True)
    like = models.ManyToManyField(Profile, blank=True, related_name="liked")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return f"{self.user}-{self.post}"
    
    def get_all_user_liked(self) :
        return self.like.all()
    
    def get_all_no_of_like(self) :
        return self.get_all_user_liked().count()

    def save(self, *args, **kwargs) :
        if not self.slug :
            self.slug = make_slug_url_comment()
        return super().save(*args, **kwargs)
    
    def get_update_comment_url(self) :
        return reverse("posts:update_comment", kwargs={"slug":self.slug})
    
    def get_delete_url_comment(self) :
        return reverse("posts:delete_comment", kwargs={"slug":self.slug})

class LikeComment(models.Model) :
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.CharField(max_length=6, choices=VALUE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.comment}-{self.user}-{self.value}"