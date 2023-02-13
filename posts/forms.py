from django.forms import ModelForm
from .models import Post, Comment

class CreatePostForm(ModelForm) :
    class Meta :
        model = Post
        fields = ["text", "image"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
        self.fields['image'].label = ''
        self.fields['text'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Create Post"})


class AddCommentForm(ModelForm) :
    class Meta :
        model = Comment
        fields = "body",
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.fields['body'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Add Comment"})
