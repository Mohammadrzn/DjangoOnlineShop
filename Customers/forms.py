from django import forms
from .models import Customer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ("username", "password")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                customer = Customer.objects.get(username=username)
                if not customer.check_password(password):
                    raise forms.ValidationError('نام کاربری یا رمز اشتباه است')
            except Customer.DoesNotExist:
                raise forms.ValidationError('نام کاربری یا رمز اشتباه است')

        return cleaned_data

    class Meta:
        fields = ("username", "password")
