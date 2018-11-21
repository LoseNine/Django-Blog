from django import forms
from .models import *
from captcha.fields import CaptchaField

class EmailForm(forms.Form):
    name=forms.CharField(max_length=125,label='名字')
    to=forms.EmailField(label='接收方')
    comments=forms.CharField(label='评论',required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model=Comment
        fields=['name','email','body']
    # def __init__(self):
    #     super(CommentForm, self).__init__()
    #     self.fields['body'].label = '评论'
    #     self.fields['name'].label = '尊姓大名'
    #     self.fields['email'].label = '您的邮箱地址'
    #     self.fields['captcha'].label = '确认你不是机器人'


