"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from mysite.views import *


# from django.views.static import serve
# from django.conf import settings
#
# from haystack.views import SearchView

urlpatterns = [
    #jet后台
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    #搜索引擎
    # url(r'^search/', include('haystack.urls')),
    path('search/',MySeachView(),name='haystack'),

    path('admin/', admin.site.urls),
    path('mysite/',include('mysite.urls',namespace='mysite'))
]
