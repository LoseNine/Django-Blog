from django import template
from ..models import *
from django.db import models

register=template.Library()

@register.simple_tag
def total_posts():

    return Articles.objects.count()

@register.filter
def total_comment(value):
    article = Articles.objects.get(slug=value)
    return article.comment_set.count()

@register.inclusion_tag('mysite/latest_article.html')
def show_latest_articles(count=5):
    latest_article=Articles.objects.all().order_by('-created_time')[:count]
    return {'latest_article':latest_article}

@register.inclusion_tag('mysite/mostcomment_article.html')
def mostcomment_articles(count=5):
    mostcomment_articles=Articles.objects.annotate(total_comments=models.Count('comment')).order_by('-total_comments')[:count]
    return {'mostcomment_articles':mostcomment_articles}