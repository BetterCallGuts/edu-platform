# IMporetr static
from django.conf import settings
from django.templatetags.static import static

from .models import GlobalVars, Logo


def global_variable(request):
    try:
        logo_obj = Logo.objects.first()
        logo = logo_obj.logo.url if logo_obj else static('mat/logo.svg')
    except:
        logo = static('mat/logo.svg')

    website = GlobalVars.objects.filter(Key="website_name").first()
    website = website.Value if website else "Taleb Azhari"

    domain = GlobalVars.objects.filter(Key="domain").first()
    domain = domain.Value if domain else "Taleb Azhari"

    copyright = GlobalVars.objects.filter(Key="copyright").first()
    copyright = copyright.Value if copyright else "Taleb Azhari"

    return {
        'website': website,
        'logo': logo,
        'domain': domain,
        'copyright': copyright,
    }