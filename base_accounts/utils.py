from django.contrib.auth import get_user_model


class UserAlreadyExists(Exception):
    """User that is being created already exists on system"""
    pass


def unique_username(src, counter):
    """
    Create a new username (30 chars max) by joining the source
    (e.g. email user part) and a counter. Additionally, if the
    password has not be supplied, assign a random one.
    """
    suffix_num = str(counter)
    username = '%s%s' % (src.split('@', 1)[0][:30 - len(suffix_num)], counter)
    return username[:30]

def create_email_user(email, password):
    """
    If the email does not exist, create a new one. Additionally,
    if the password has not been supplied, assign a random one.
    """
    user_model = get_user_model()
    try:
        user_model.objects.get(email__iexact=email.lower())
    except user_model.DoesNotExist:
        # Create a username by joining email user and the total of user entries
        obj_count = user_model.objects.count()
        username = unique_username(email, obj_count)
        if password is None:
            password = user_model.objects.make_random_password()
        user = user_model.objects.create_user(username, email, password)
        return user
    else:
        raise UserAlreadyExists

