from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from taggit.managers import TaggableManager
from slugify import slugify

# Create your models here.

class Articles(models.Model):
    CHOICE_STATUS=(
        ('草稿','草稿'),
        ('成文','成文'),
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=250,unique=True,blank=True)
    content=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created_time=models.DateTimeField(auto_now_add=True)
    change_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=CHOICE_STATUS,default='草稿')
    tags=TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering=['created_time']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug=slugify(self.title)
        super(Articles, self).save()

class Comment(models.Model):
    article=models.ForeignKey(Articles,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.article,self.name)
