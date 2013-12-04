=============
Configuration
=============

Settings
========

BASE_ACCOUNTS_SIGNUP_REDIRECT_URL
---------------------------------

* default: settings.LOGIN_REDIRECT_URL

BASE_ACCOUNTS_LOGIN_REDIRECT_URL
--------------------------------

* default: settings.LOGIN_REDIRECT_URL

BASE_ACCOUNTS_POST_LOGIN_REDIRECT_URL
-------------------------------------

* default: settings.LOGIN_REDIRECT_URL

BASE_ACCOUNTS_LOGOUT_REDIRECT_URL
---------------------------------

* default: settings.LOGOUT_URL

BASE_ACCOUNTS_UPDATE_EMAIL_REDIRECT_URL = '/accounts/settings/'
BASE_ACCOUNTS_UPDATE_PASSWORD_REDIRECT_URL = '/accounts/settings/'
BASE_ACCOUNTS_UPDATE_EMAIL_ERROR_REDIRECT_URL = '/accounts/settings/'
BASE_ACCOUNTS_UPDATE_PASSWORD_ERROR_REDIRECT_URL = '/accounts/settings/'

Post model
==========

You must subclass ``Post`` model::

    class MyPost(Post):
        pass

Let ``django-nomadblog`` know that it will be the model to use::

    POST_MODEL = 'yourapp.models.MyPost'

You can optionally extend the model::

    class MyPost(Post):
        summary = models.TextField()
        ...

Multiblog
=========

A simple project setting and a URL pattern is all we need to configure our
django-omadblog installation for single or multiple blog management.

If you want to maintain multiple blogs, enable the following variable in
your project settings::

    NOMADBLOG_MULTIPLE_BLOGS = True

Multiblog-enabled configurations require that the urls pass the
``blog_slug`` to the views, because they will need to know
which blog they are going to process::

    # Add this pattern into your root url conf
    urlpatterns = patterns('',
        ...
        (r'^blogs/(?P<blog_slug>[-\w]+)/', include('nomadblog.urls')),

Otherwise to store a single blog just do::

    (r'^blog', include('nomadblog.urls')),

Post status
===========

By default posts can be draft, private or public, only public ones are listed
or displayed.  You can override your status choices as well as which one of
the choices is the display filter for listings::

    POST_STATUS_CHOICES = (
        (0, 'Borrador'),
        (1, 'Pendiente de revision'),
        (2, 'Revisado'),
        (3, 'Publicado'),
    )
    PUBLIC_STATUS = 3

