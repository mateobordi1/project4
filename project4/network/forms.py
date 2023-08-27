from django import forms
from .models import User , Post, Follow

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = '__all__'