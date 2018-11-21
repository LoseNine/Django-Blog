from django import forms
from .models import *

class EmailForm(forms.Form):
    name=forms.CharField(max_length=125,label='名字')
    to=forms.EmailField(label='接收方')
    comments=forms.CharField(label='评论',required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','body']
