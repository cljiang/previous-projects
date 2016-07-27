import os
import uuid 
import datetime

from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('documents/', filename)

class Document(models.Model):
    post = models.ForeignKey('blog.Post', related_name='documents')
    docfile = models.FileField(upload_to=get_file_path)

class mylist(models.Model):
    post = models.ForeignKey('blog.Post', related_name='mylists')
    pdffile = models.FileField(upload_to=get_file_path)

class Album(TimeStampedModel):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True,null=True)
    cover_photo = models.ForeignKey('blog.Post', related_name='albums',blank=True, null=True)
    is_public = models.BooleanField(default=True)
    date_added = models.DateField(null=True,blank=True)
    tags = TaggableManager(blank=True,help_text=None)
    order = models.PositiveIntegerField(default=9999)

class Photo(TimeStampedModel):
    album = models.ForeignKey(Album)
    photofile = models.ImageField(upload_to='photo/%Y/%m/%d')
    description = models.TextField(blank=True,null=True)
    is_public = models.BooleanField(default=True)
    tags = TaggableManager(blank=True,help_text=None)

