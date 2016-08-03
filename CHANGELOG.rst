=========
CHANGELOG
=========

Version 2.3.10
=============

* Modify logout view to update first_login only if exists.

Version 2.3.9
=============

* Fix email verification in registration form - duplicate email
  check is no longer case sensitive.

Version 2.3.8
=============

* Fix logout after pwd change view in Django 1.7

Version 2.3.7
=============

* Make sure to count User when generation appended num to user
* Do not use username as name when name is not provided

Version 2.3.6
=============

* Added missing locale files to setup.py

Version 2.3.5
=============

* Fixed bug in login form clean method causing server error when
  empty fields were posted

Version 2.3.4
=============

* Added BASE_ACCOUNTS_CONFIRM_EMAIL_REDIRECT_URL setting

Version 2.3.3
=============

* Fixed some bugs
* Refactored some of signup form code into a mixin

Version 2.3.2
=============

* Forms now can override user model and pass it to utils.create_email_user
* Some code cleanup at utils.py

Version 2.3.1
=============

* Move auth validations to form cleaning methods, avoid redirect on error
* Fix next param so invalid forms submissions don't lose proper redirections

Version 2.3.0
=============

* Add email confirmation capabilities
* Fix documentation

Version 2.2.1
=============

* Add spanish translations

Version 2.0.0
=============

* Backwards-incompatible changes on CBV
* Add default templates

Version 1.1.0
=============

* Expose username creation as standalone function in utils.py

Version 1.0.0
=============

* Production use

Version 0.9.0
=============

* First release of package.

