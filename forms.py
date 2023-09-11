from django import forms
from .models import Comment, Post
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')



'''class AddPostForm(forms.Form):
    Title = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'id':'titleField','placeholder':'Title of Post...'}))
    Body = forms.CharField(widget=forms.Textarea(attrs={'id':'bodyfield'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'id_title'}))
    body = forms.CharField(widget=forms.TextInput(attrs={'id':'id_body'}))  
    
'''

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','author','slug', 'body')

        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
class post_edit(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'id_title'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'id':"id_body"}))
  
    class Meta:
        model = Post
        fields = ('title', 'body')

class deletePost(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'titleField'}))
