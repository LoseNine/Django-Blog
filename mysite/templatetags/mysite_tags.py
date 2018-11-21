from django import template
from ..models import *

register=template.Library()

@register.simple_tag
def total_posts():
    return Articles.objects.count()

@register.inclusion_tag('mysite/latest_article.html')
def show_latest_articles(count=5):
    latest_article=Articles.objects.all().order_by('-created_time')[:count]
    return {'latest_article':latest_article}