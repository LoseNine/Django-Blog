from django.contrib import admin
from .models import *
# Register your models here.

class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['user','title','created_time','change_time','slug','status','publish']
    list_filter = ['user','title','slug','status']
    ordering = ['status','publish']


admin.site.register(Articles,ArticlesAdmin)
admin.site.register(Comment)