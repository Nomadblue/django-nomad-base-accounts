=============
Configuration
=============

Add ``base_accounts`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'base_accounts',
        ...
    )

Add also to your ``urls.py``::

    url(r'^accounts/', include('accounts.auth_urls'))

User subclass
=============

Class ``BaseUser``, which subclasses ``django.contrib.auth.models.AbstractUser``, is itself abstract. Therefore, you must subclass ``BaseUser`` from another class of yours. This allows you to add extra funtionality, include mixins, override methods, or any other stuff you need. For example, we usually create an ``accounts`` app inside our project, and from a ``models.py``::

    from django.db import models
    from base_accounts.models import BaseUser

    class User(BaseUser):
        pass

Do not forget to include your new app into your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'base_accounts',
        'accounts',
        ...
    )

Now tell your project that this will be your auth model, and include the backend for authentication::

    AUTH_USER_MODEL = 'accounts.User'
    AUTHENTICATION_BACKENDS = (
        ...
        'accounts.auth_backend.EmailBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

Finally, you must sync your database with your new model. If you use south::

    python manage.py schemamigration accounts --initial
    python manage.py migrate accounts

Optional settings
=================

BASE_ACCOUNTS_SIGNUP_REDIRECT_URL
---------------------------------

* default: ``settings.LOGIN_REDIRECT_URL`` (if not set, '/accounts/profile/' in Django by default)

BASE_ACCOUNTS_LOGIN_REDIRECT_URL
--------------------------------

* default: ``settings.LOGIN_REDIRECT_URL`` (if not set, '/accounts/profile/' in Django by default)

BASE_ACCOUNTS_POST_LOGIN_REDIRECT_URL
-------------------------------------

* default: ``settings.LOGIN_REDIRECT_URL`` (if not set, '/accounts/profile/' in Django by default)

BASE_ACCOUNTS_LOGOUT_REDIRECT_URL
---------------------------------

* default: ``settings.LOGOUT_URL`` (if not set, '/accounts/logout/' in Django by default)

BASE_ACCOUNTS_UPDATE_EMAIL_REDIRECT_URL
---------------------------------------

* default: Reverse of ``settings_update_email`` view

BASE_ACCOUNTS_UPDATE_EMAIL_ERROR_REDIRECT_URL
---------------------------------------------

* default: Reverse of ``settings_update_email`` view

BASE_ACCOUNTS_UPDATE_PASSWORD_REDIRECT_URL
------------------------------------------

* default: Reverse of ``settings_update_password`` view

BASE_ACCOUNTS_UPDATE_PASSWORD_ERROR_REDIRECT_URL
------------------------------------------------

* default: Reverse of ``settings_update_password`` view
