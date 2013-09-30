from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from base_accounts.views import LoginFormView, SignupFormView, LogoutView, UpdateEmailFormView, UpdatePasswordFormView, PostLoginRedirectView


urlpatterns = patterns('base_accounts.views',
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^post-login/$', PostLoginRedirectView.as_view(), name='post_login'),
    url(r'^signup/$', SignupFormView.as_view(), name='signup'),
    url(r'^settings/$', login_required(TemplateView.as_view(template_name='accounts/settings/edit_settings.html')), name='settings'),
    url(r'^settings/update/email/$', login_required(UpdateEmailFormView.as_view()), name='settings_update_email'),
    url(r'^settings/update/password/$', login_required(UpdatePasswordFormView.as_view()), name='settings_update_password'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name="logout"),
)

