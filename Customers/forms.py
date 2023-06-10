from django import forms


class SendOTPForm(forms.Form):
    mail_phone = forms.CharField(error_messages={
        'required': 'وارد کردن این فیلد الزامی',
        'invalid': 'شماره همراه یا ایمیل معتبر نمی باشد.'
    })


class VerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=6, error_messages={
        'required': 'وارد کردن این فیلد الزامی',
        'max_length': 'کد وارد شده بیش از حد مجاز می باشد.'
    })
