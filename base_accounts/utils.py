from django.contrib.auth import get_user_model


class UserAlreadyExists(Exception):
    """
    User that is being created already exists on system
    """
    pass


def unique_username(email, counter):
    """
    Create a new username (30 chars max) by joining the left user part
    of an email address and a counter.
    """
    suffix_num = str(counter)
    username = '%s%s' % (email.split('@', 1)[0][:30 - len(suffix_num)], counter)
    return username[:30]


def create_email_user(email, password, user_model=get_user_model(), **extrafields):
    """
    Generate a unique username and create a new instance of ``user_model``
    with email, password and any other extra fields
    """
    try:
        user_model.objects.get(email__iexact=email.lower())
    except user_model.DoesNotExist:
        base_user = get_user_model()  # Make sure to count User, not inheriting models
        obj_count = base_user.objects.count()
        username = unique_username(email, obj_count)
        user = user_model.objects.create_user(username, email, password, **extrafields)
        return user
    else:
        raise UserAlreadyExists
