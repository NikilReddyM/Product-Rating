from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import ModelForm
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CommentForm(forms.Form):
    comment =forms.CharField(
        widget=forms.Textarea,
        max_length=500
    )

    def clean(self):
        return self.cleaned_data['comment']


