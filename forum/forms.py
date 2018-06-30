from django import forms
from .models import Post, Reply, Bulletin, Message
from basicInfo.models import attrib as Attrib, account as Account


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
