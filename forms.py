from django import forms

from .models import Post, Comment, Document, Album, Photo, mylist

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class mylistForm(forms.Form):
    pdffile = forms.FileField(
         label='Save a pdf'
    )

class AlbumForm(forms.Form):
    albumfile = forms.FileField(
        label='Select a file'
    )

class PhotoForm(forms.Form):
    photofile = forms.FileField(
        label='Select a file'
    )


