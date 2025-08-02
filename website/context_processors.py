# IMporetr static
from django.conf import settings
from django.templatetags.static import static




def global_variable(request):

    return {
        'website': 'TESTBRANDNAME',
        'logo': static('mat/logo.svg'),
    }