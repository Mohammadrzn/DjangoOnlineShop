from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ("username", "password")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ("username", "password")
