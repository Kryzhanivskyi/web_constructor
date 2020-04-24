from django.conf import settings
from nodeads_libs.web_lib_core.views import get_template, get_lang


def template_manager(request, slug):
    lang = get_lang(request, settings.DEFAULT_LANGUAGE)
    response = get_template(slug, lang, request)
    response.set_cookie('lang', lang)
    return response


def main(request):
    slug = '/'
    response = template_manager(request, slug)
    return response


def slug_main(request, slug):
    response = template_manager(request, slug)
    return response


