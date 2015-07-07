from django.db import models
from django.core import signing
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class BaseUser(AbstractUser):
    slug = models.SlugField(_('slug'), max_length=255)
    name = models.CharField(_('name'), max_length=255, blank=True)
    first_login = models.BooleanField(_('first login'), default=True)
    image = models.ImageField(_('image'), blank=True, null=True, upload_to="images/avatars/%Y/%m/%d", max_length=255)
    confirmed = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        # Create slug from username. Although ``BaseUser.slug`` field is not
        # unique at database level, it will be unique as long as
        # ``AbstractUser.username`` stays unique as well.
        if not self.id:
            self.slug = slugify(self.username)

        super(BaseUser, self).save(*args, **kwargs)

    def get_display_name(self):
        return self.name or self.username

    def get_confirmation_token(self):
        return signing.dumps(self.pk)
