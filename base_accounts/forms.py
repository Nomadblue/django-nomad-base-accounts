from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class SignupForm(forms.Form):
    full_name = forms.CharField(label=_('full name'))
    email = forms.EmailField(label=_('email'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    tos = forms.BooleanField(label=_('I accept the terms of service'))


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('email'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)


class UpdateEmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.user = request.user
        return super(UpdateEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self, *args, **kwargs):
        data = self.cleaned_data['email']
        user_model = get_user_model()
        try:
            user_model.objects.exclude(id=self.user.id).get(email=data)
        except user_model.DoesNotExist:
            return data
        else:
            raise forms.ValidationError(_("Email is already being used by another user"))


class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(label=_('new password'), widget=forms.PasswordInput,)
    password2 = forms.CharField(label=_('new password (confirm)'), widget=forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.user = request.user
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(_("Passwords didn't match"))
        return password2

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        user_model = get_user_model()
        user_model.objects.filter(pk=self.user.pk).update(password=self.user.password)
