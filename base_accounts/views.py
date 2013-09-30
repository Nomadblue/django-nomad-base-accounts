# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.views.generic.base import RedirectView
# from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from django.conf import settings

from base_accounts.forms import SignupForm, LoginForm, UpdateEmailForm, UpdatePasswordForm
from base_accounts.utils import create_email_user, UserAlreadyExists


class SignupFormView(FormView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def get_success_url(self):
        if self.request.POST.get('next'):
            self.success_url = self.request.POST.get('next')
        return super(SignupFormView, self).get_success_url()

    def get_context_data(self, **kwargs):
        ctxt = super(SignupFormView, self).get_context_data(**kwargs)
        ctxt['next'] = self.request.GET.get('next') or ''
        return ctxt

    def form_valid(self, form):
        """Register and login new user and send welcome email"""

        # Create new user
        full_name = form.cleaned_data.get('full_name').lower()
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password')
        try:
            user = create_email_user(email, password)
        except UserAlreadyExists:
            messages.error(self.request, _("This email already exists on our systems"))
            return redirect('signup')
        user.name = full_name
        user.save()

        # Login user
        user = authenticate(username=user.username, password=password)
        login(self.request, user)

        messages.success(self.request, _("Welcome!"))
        return super(SignupFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def get_success_url(self):
        if self.request.POST.get('next'):
            self.success_url = self.request.POST.get('next')
        return super(LoginFormView, self).get_success_url()

    def get_context_data(self, **kwargs):
        ctxt = super(LoginFormView, self).get_context_data(**kwargs)
        ctxt['next'] = self.request.GET.get('next') or ''
        return ctxt

    def form_valid(self, form):
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(self.request, _("Please insert both valid email and password"))
                return redirect('login')
            elif not user.is_active:
                messages.error(self.request, _("Your account is inactive"))
                return redirect('login')
        login(self.request, user)
        messages.success(self.request, _("Welcome back, %(display_name)s!") % {'display_name': user.get_display_name()})
        return super(LoginFormView, self).form_valid(form)


class PostLoginRedirectView(RedirectView):
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            self.url = self.request.GET.get('next')
        return super(PostLoginRedirectView, self).dispatch(request, *args, **kwargs)


class UpdateEmailFormView(FormView):
    form_class = UpdateEmailForm

    def get_form_kwargs(self):
        kwargs = super(UpdateEmailFormView, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs

    def form_invalid(self, form):
        for error in form.errors.get('email'):
            messages.error(self.request, error)
        return redirect('settings')

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data.get('email')
        self.request.user.save()
        messages.success(self.request, _("You have updated your email"))
        return redirect('settings')


class UpdatePasswordFormView(FormView):
    form_class = UpdatePasswordForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordFormView, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs

    def form_invalid(self, form):
        messages.success(self.request, _("Passwords didn't match"))
        return redirect('settings')

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['password1'])
        self.request.user.save()
        messages.success(self.request, _("You have updated your password"))
        return redirect('settings')


class LogoutView(RedirectView):
    success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.first_login:
            user.first_login = False
            user.save(update_fields=['first_login'])
        logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

