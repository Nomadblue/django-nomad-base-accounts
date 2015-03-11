=========
CHANGELOG
=========

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

