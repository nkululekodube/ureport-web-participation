from django.conf import settings


def undashify_user(user):
    return user.replace('-', '')


def dashify_user(user):
    return user[:8] + '-' + user[8:12] + '-' + user[12:16] + '-' + user[16:20] + '-' + user[20:]


def get_url(path):
    return '%s%s' % (settings.WEBPARTICIPATION_ROOT, path)
