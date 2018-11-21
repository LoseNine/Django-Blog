from django.urls import path
from .views import *

app_name='mysite'
urlpatterns=[
    path('',ArticleList.as_view(),name='articlelist'),
    path('article/<slug:slug>/',ArticleDetial.as_view(),name='articledetial'),
    path('/share/<int:pk>/',article_share.as_view(),name='articleshare'),
]