from django.contrib.auth import get_user_model


class UserAlreadyExists(Exception):
    """User that is being created already exists on system"""
    pass


def create_email_user(email, password):
    """
    If the email does not exist, create a new user with a username
    (30 chars max) by joining email user and a counter. Additionally,
    if the password has not be supplied, assign a random one.
    """
    user_model = get_user_model()
    try:
        user_model.objects.get(email__iexact=email.lower())
    except user_model.DoesNotExist:
        # Create a username (30 chars max) by joining email user and a counter.
        suffix_num = str(user_model.objects.count())
        username = '%s%s' % (email.split('@', 1)[0][:30 - len(suffix_num)], user_model.objects.count())
        username = username[:30]
        if password is None:
            password = user_model.objects.make_random_password()
        user = user_model.objects.create_user(username, email, password)
        return user
    else:
        raise UserAlreadyExists

