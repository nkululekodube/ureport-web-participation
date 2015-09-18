from django.conf import settings

def ureport(request):
    return {'UREPORT_URL': settings.UREPORT_ROOT}
