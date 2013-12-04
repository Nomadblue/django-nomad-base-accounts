# -*- coding: utf-8 -*-

from django.views.generic import View, FormView
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from base_accounts.forms import SignupForm, LoginForm, UpdateEmailForm, UpdatePasswordForm
from base_accounts.utils import create_email_user, UserAlreadyExists


from django.contrib import messages
try:
    from django.contrib.messages.views import SuccessMessageMixin
except:
    # This mixin was added to Django 1.6, we define it for backwards compatibility

    class SuccessMessageMixin(object):
        """
        Adds a success message on successful form submission.
        """
        success_message = ''

        def form_valid(self, form):
            response = super(SuccessMessageMixin, self).form_valid(form)
            success_message = self.get_success_message(form.cleaned_data)
            if success_message:
                messages.success(self.request, success_message)
            return response

        def get_success_message(self, cleaned_data):
            return self.success_message % cleaned_data


class ErrorMessageRedirectMixin(object):
    """Redirect to error url if exists, converting form error strs to sys msgs"""

    def form_invalid(self, form):
        if self.error_url:
            for msg in form.errors.values():
                messages.error(self.request, _(msg[0]))
            return redirect(self.error_url)
        return super(ErrorMessageRedirectMixin, self).form_invalid(form)


class NextRedirectMixin(object):
    """Manages redirection on post-login or post-signup"""

    def get_success_url(self):
        if self.request.POST.get('next'):
            self.success_url = self.request.POST.get('next')
        return super(NextRedirectMixin, self).get_success_url()

    def get_context_data(self, **kwargs):
        ctxt = super(NextRedirectMixin, self).get_context_data(**kwargs)
        ctxt['next'] = self.request.GET.get('next') or ''
        return ctxt


class SignupFormView(SuccessMessageMixin, NextRedirectMixin, FormView):
    form_class = SignupForm
    template_name = 'base_accounts/signup.html'
    success_url = getattr(settings, 'BASE_ACCOUNTS_SIGNUP_REDIRECT_URL', settings.LOGIN_REDIRECT_URL)
    success_message = _("Welcome!")

    def form_valid(self, form):
        full_name = form.cleaned_data.get('full_name').lower()
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password')

        # Check that email does not exist on system
        try:
            user = create_email_user(email, password)
        except UserAlreadyExists:
            messages.error(self.request, _("This email already exists on our systems"))
            return redirect('signup')

        # Set full name
        user.name = full_name
        user.save(update_fields=['name'])

        # Login user
        user = authenticate(username=user.username, password=password)
        login(self.request, user)

        return super(SignupFormView, self).form_valid(form)


class LoginFormView(SuccessMessageMixin, NextRedirectMixin, FormView):
    form_class = LoginForm
    template_name = 'base_accounts/login.html'
    success_url = getattr(settings, 'BASE_ACCOUNTS_LOGIN_REDIRECT_URL', settings.LOGIN_REDIRECT_URL)
    success_message = _("You have logged in")

    def form_valid(self, form):
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password')

        # Check that email and password match and user is active
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(self.request, _("Please insert both valid email and password"))
                return redirect('login')
            elif not user.is_active:
                messages.error(self.request, _("Your account is inactive"))
                return redirect('login')

        # Login user
        login(self.request, user)

        return super(LoginFormView, self).form_valid(form)


class UpdateEmailFormView(SuccessMessageMixin, ErrorMessageRedirectMixin, FormView):
    """Updates user model with new provided email"""
    form_class = UpdateEmailForm
    template_name = 'base_accounts/update_email.html'
    success_url = getattr(settings, 'BASE_ACCOUNTS_UPDATE_EMAIL_REDIRECT_URL', reverse_lazy('settings_update_email'))
    error_url = getattr(settings, 'BASE_ACCOUNTS_UPDATE_EMAIL_ERROR_REDIRECT_URL', '')
    success_message = _('You have updated your email successfully')

    def get_form_kwargs(self):
        """Form uses request to fetch current user"""
        kwargs = super(UpdateEmailFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data.get('email')
        self.request.user.save(update_fields=['email'])
        return super(UpdateEmailFormView, self).form_valid(form)


class UpdatePasswordFormView(SuccessMessageMixin, ErrorMessageRedirectMixin, FormView):
    """Updates user model with new provided password"""
    form_class = UpdatePasswordForm
    template_name = 'base_accounts/update_password.html'
    success_url = getattr(settings, 'BASE_ACCOUNTS_UPDATE_PASSWORD_REDIRECT_URL', reverse_lazy('settings_update_password'))
    error_url = getattr(settings, 'BASE_ACCOUNTS_UPDATE_PASSWORD_ERROR_REDIRECT_URL', '')
    success_message = _('You have updated your password successfully')

    def get_form_kwargs(self):
        """Form uses request to fetch current user"""
        kwargs = super(UpdatePasswordFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        """Use model method to update new password"""
        self.request.user.set_password(form.cleaned_data['password1'])
        self.request.user.save(update_fields=['password'])
        return super(UpdatePasswordFormView, self).form_valid(form)


class PostLoginRedirectView(SuccessMessageMixin, View):
    """Used by social login flows (e.g. OAuth)"""
    success_url = getattr(settings, 'BASE_ACCOUNTS_POST_LOGIN_REDIRECT_URL', settings.LOGIN_REDIRECT_URL)
    success_message = _("You have logged in")

    def dispatch(self, request, *args, **kwargs):
        """Override post-login url if provided"""
        if self.request.GET.get('next'):
            self.success_url = self.request.GET.get('next')
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)


class LogoutView(View):
    """Updates User.first_login field before logout"""
    success_url = getattr(settings, 'BASE_ACCOUNTS_LOGOUT_REDIRECT_URL', '/')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.first_login:
            user.first_login = False
            user.save(update_fields=['first_login'])
        logout(request)
        return redirect(self.success_url)
