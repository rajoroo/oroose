from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class OtpForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=100)
