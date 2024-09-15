from django import forms

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
