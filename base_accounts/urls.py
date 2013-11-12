from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from base_accounts.views import LoginFormView, SignupFormView, LogoutView, UpdateEmailFormView, UpdatePasswordFormView, PostLoginRedirectView


urlpatterns = patterns(
    'base_accounts.views',
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^post-login/$', PostLoginRedirectView.as_view(), name='post_login'),
    url(r'^signup/$', SignupFormView.as_view(), name='signup'),
    url(r'^settings/email/$', login_required(UpdateEmailFormView.as_view()), name='settings_update_email'),
    url(r'^settings/password/$', login_required(UpdatePasswordFormView.as_view()), name='settings_update_password'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name="logout"),
)
