from django import forms
from .models import Post, Reply, Bulletin, Message

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('text',)

class BulletinForm(forms.ModelForm):
    
    class Meta:
        model = Bulletin
        fields = ('title', 'text',)

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('receiver', 'text',)