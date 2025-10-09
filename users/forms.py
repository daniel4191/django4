from django import forms
from django.core.exceptions import ValidationError

from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget = forms.TextInput(
            attrs = {"placeholder": "아이디 입력해주세요 (3자리 이상)"},
        ),
        )
    password = forms.CharField(
        min_length=4,
        widget = forms.PasswordInput(
            attrs = {"placeholder": "비밀번호 입력해주세요 (4자리 이상)"},
        ),
        )
    
class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    profile_image = forms.ImageField()
    short_description = forms.CharField()
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username = username).exists():
            raise ValidationError(f"{username}아이디는 이미 존재 합니다.")
        return username
        
    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            self.add_error("password2", "비밀번호 입력값 다름")
            
    def save(self):
        username = self.cleaned_data["username"]
        password1 = self.cleaned_data['password1']
        profile_image = self.cleaned_data["profile_image"]
        short_description = self.clean_username["short_description"]
        user = User.objects.create_user(
            username = username,
            password = password1,
            profile_image = profile_image,
            short_description = short_description
        )
        return user