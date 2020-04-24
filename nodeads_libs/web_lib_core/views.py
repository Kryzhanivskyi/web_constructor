from django.http import HttpResponse
from django.shortcuts import redirect
from .utils import parse_html
from .const import MODELS_WITH_LANG
from .models import (Page, Content, ContentLang, ContentItem, PageLang, Language, DImageGroup, DVideoGroup, DMusicGroup,
                     DImageGroupLang, DVideoGroupLang, DMusicGroupLang, DImage, DVideo, DMusic, DImageLang,
                     DVideoLang, DMusicLang, PageParam, ContentItemLang, DPost, DPostLang, DPostTag, DPostTagLang,
                     DPostImage, DPostVideo)
import re
import datetime
import cgi


def set_language(request):
    '''    href="{% url 'set_language' %}?lang={{ language.code|lower }}&next={{ request.path }}"  '''
    language = request.GET.get('lang', request.COOKIES.get('lang'))
    response = redirect(request.GET.get('next', '/') + f'?lang={language}')
    response.set_cookie('lang', request.GET.get('lang', 'ru'))
    return response


def matrix_to_html(request):
    lang_code = request.GET.get('lang', request.COOKIES.get('lang')).upper()
    template_name = request.GET.get('template_name', None)
    template = '<h1>Error</h1>'
    if template_name:
        item_lang_q = ContentItemLang.objects.all()
        matrix = item_lang_q.filter(ui_item__ui__ui_type__name='matrix_element',
                                    ui_item__name=template_name)
        template = item_lang_q.filter(ui_item__ui__ui_type__name='complete_page',
                                      ui_item__ui__name=f'{template_name}.html')
        for matrix_lang in matrix:
            page_lang = template.filter(lang=matrix_lang.lang).first()
            page_lang.html = parse_html(html=matrix_lang.html, item_queryset=item_lang_q.filter(lang__code=lang_code))
            page_lang.save()

    return HttpResponse(template.filter(lang__code=lang_code).first().html)


def get_lang(request, default_lang):
    lang = request.GET.get('lang', request.COOKIES.get('lang'))
    if not lang:
        lang = default_lang
    return lang


def get_template(slug, lang, request):
    pages = Page.objects.filter(url=slug, is_reg_exp=False)
    if pages:
        page = pages[0]
        content_type = page.root_content.content_type.name
        formed_page = get_formed_page(page, lang, slug, request)
        if content_type == 'css':
            return HttpResponse(formed_page, content_type="text/css")
        elif content_type == 'javascript':
            return HttpResponse(formed_page, content_type="application/javascript")
        else:
            return HttpResponse(formed_page)
    else:
        pages = Page.objects.filter(is_reg_exp=True)
        if pages:
            for page in pages:
                regular = page.url
                result = re.findall(regular, slug)
                if result:
                    content_type = page.root_content.content_type.name
                    formed_page = get_formed_page(page, lang, slug, request)
                    if content_type == 'css':
                        return HttpResponse(formed_page, content_type="text/css")
                    elif content_type == 'javascript':
                        return HttpResponse(formed_page, content_type="application/javascript")
                    else:
                        if result[0][0].split('/')[0] == 'post':
                            post_counter(result[0][1], lang)
                        return HttpResponse(formed_page)
            return HttpResponse('404')
        else:
            return HttpResponse('404')


def get_formed_page(page, lang, slug, request):
    page_params = PageView(page, slug)
    result_1 = gen_step_1(page, lang, slug, page.root_content.html, page_params)
    result_2 = gen_step_2(result_1, lang, slug, page_params)
    result_3 = gen_step_3(result_2, request)
    return result_3


def gen_step_1(page, lang, slug, gen_html, page_params):
    gen_html = replace_page_param(gen_html, page_params)
    items_list_to_replace = re.findall('{%(?P<table>\w+)(?P<id_param>\((?P<id>\d+)\))?\.(?P<field>\w+)%}', gen_html)
    if items_list_to_replace:
        for item in items_list_to_replace:
            list_model_pieces = item[0].split('_')
            list_model = ''.join([x.capitalize() for x in list_model_pieces])
            item_id = item[2]
            item_field = item[3]
            if list_model == 'Content':
                if list_model in MODELS_WITH_LANG:
                    my_filter = {'content_id': item_id, 'lang__code': lang}
                    if getattr(eval(list_model + 'Lang').objects.filter(**my_filter).first(), item_field.lower(), False):
                        item_to_replace = eval(list_model+'Lang').objects.get(content_id=item_id, lang__code=lang)
                        attr = getattr(item_to_replace, item_field.lower())
                    else:
                        item_to_replace = eval(list_model).objects.get(pk=item_id)
                        attr = getattr(item_to_replace, item_field.lower())
                else:
                    item_to_replace = eval(list_model).objects.get(pk=item_id)
                    attr = getattr(item_to_replace, item_field.lower())
                if type(attr) is datetime.datetime:
                    gen_html = gen_html.replace('{%' + f'{item[0]}({item_id}).{item_field}' + '%}',
                                                  str(int(attr.timestamp())))
                    continue
                html_item = getattr(item_to_replace, 'html_item')
                replace_list = gen_step_2(attr, lang, slug, page_params, html_item)
                gen_html = gen_html.replace('{%' + f'{item[0]}({item_id}).{item_field}' + '%}',
                                              replace_list)
            if list_model == 'PageLang':
                item_to_replace = PageLang.objects.get(lang__code=lang.upper(), page__id=page.id)
                if item_field.lower() == 'description' or item_field.lower() == 'keywords':
                    attr = getattr(item_to_replace, item_field.lower())
                    attr = cgi.html.escape(attr, True)
                else:
                    attr = getattr(item_to_replace, item_field.lower())
                gen_html = gen_html.replace('{%' + f'{item[0]}.{item_field}' + '%}', attr)
        return gen_step_1(page, lang, slug, gen_html, page_params)
    else:
        return gen_html


def gen_step_2(page_html, lang, slug, page_params, html_item=''):
    page_html = replace_page_param(page_html, page_params)
    list_to_replace = re.findall('(?P<all>{%\s*(?P<table>\w+)@((?P<master_field>\w+)\((?P<id>\d+)?\))?(\s?(ASC|DESC)\s(?P<order_index>\w+)?(\s(?P<limit>\w+)\s(\d+))?)?\s*%})', page_html)  # test
    if list_to_replace:
        for lst in list_to_replace:
            list_model_pieces = lst[1].split('_')
            table = ''.join([x.capitalize() for x in list_model_pieces])
            full_expression, field_orig, master_field, master_id, order_type, order = lst[0], lst[2], lst[3], lst[4],\
                                                                                      lst[6], lst[7]
            limit = lst[9]
            if limit and lst[10]:
                limit_count = int(lst[10])
            else:
                limit_count = 0
            where = dict()
            if getattr(eval(table), 'is_visible', False):    # проверить есть ли у модели такое поле
                where['is_visible'] = True
            if field_orig:
                my_list = master_field.split('_')
                my_list.remove(my_list[-1])
                key = '_'.join([x.lower() for x in my_list])
                where[key] = master_id
            data = eval(table).objects.filter(**where)
            if order_type:
                if order_type == 'ASC':
                    data = data.order_by(order.lower())
                elif order_type == 'DESC':
                    data = data.order_by(order.lower()).reverse()  # reverse
                if limit:
                    data = data[:limit_count]
            if getattr(eval(table), 'html_item', False):
                item_sample = eval(master_field.split('_')[0].capitalize()).objects.get(pk=master_id).html_item
            else:
                item_sample = html_item
            fields = re.findall('{%(\w+)%}', item_sample)
            result = ''
            for item in data:
                sample = item_sample
                for field in fields:
                    if isinstance(item, ContentItem):   # только для модели ContentItem
                        if getattr(item, 'is_single_lang') is False:   # если не стоит галочка на is_single_lang
                            item_lang = ContentItemLang.objects.filter(content_item=item, lang__code=lang.upper()).first()
                            if item_lang:
                                if not getattr(item_lang, field.lower()):
                                    sample = sample.replace('{%' + f'{field}' + '%}', str(getattr(item, field.lower())))
                                else:
                                    sample = sample.replace('{%' + f'{field}' + '%}', str(getattr(item_lang, field.lower())))
                            else:   # если не стоит галочка на is_single_lang но поля пустые
                                sample = sample.replace('{%' + f'{field}' + '%}', str(getattr(item, field.lower())))
                    elif any(isinstance(item, eval(inst)) for inst in MODELS_WITH_LANG):  # есть ли у модели lang
                        reference_table = '_'.join([x.lower() for x in list_model_pieces][1:])
                        my_filter = {reference_table: item, 'lang__code': lang}
                        item_lang = eval(table+'Lang').objects.filter(**my_filter).first()
                        if getattr(item_lang, field.lower(), False):  # если ли у lang нужного поле для замены
                            sample = sample.replace('{%' + f'{field}' + '%}', str(getattr(item_lang, field.lower())))
                        else:  # если поля у lang нет
                            sample = sample.replace('{%' + f'{field}' + '%}', str(getattr(item, field.lower())))
                    else:
                        sample = sample.replace('{%' + f'{field}' + '%}', str(getattr(item, field.lower())))
                result += sample
            page_html = page_html.replace(full_expression, result)
        return gen_step_2(page_html, lang, slug, page_params)
    else:
        return page_html


def gen_step_3(result_2, request):
    domain = request.scheme + '://' + request.META['HTTP_HOST']
    result_2 = result_2.replace('{%$MEDIA%}', domain + '/media/')
    result_2 = result_2.replace('{%$DOMAIN%}', domain + '/')
    result_2 = result_2.replace('{%$YEAR%}', str(datetime.date.today().year))
    return result_2


def replace_page_param(gen_html, page_params):
    itm_to_replace = re.findall('({%[\w\W\S\s][^%}]*#(?P<param>\w+)[\w\W\S\s]?[^{%]*%})', gen_html)
    if itm_to_replace:
        for itm in itm_to_replace:
            full_expression = itm[0]
            item_key = itm[1]
            result = page_params.get_page_param_value(item_key)
            expression = re.findall('({%[\s]*[^\w%}]*#(?P<param>\w+)[\s]?[^\w{%]*%})', full_expression)
            if expression:
                gen_html = gen_html.replace(full_expression, result)
            else:
                gen_html = gen_html.replace('#' + item_key, result)
    return gen_html


class PageView:
    def __init__(self, page, slug):
        self.result = {}
        self.params = PageParam.objects.filter(page=page.id)
        for param in self.params:
            if param.is_reg_exp:
                regular = re.findall(param.value, slug)
                if regular:
                    for v in regular:
                        self.result[param.name] = v
            else:
                self.result[param.name] = param.value

    def get_page_param_value(self, itm_key):
        return self.result.get(itm_key)


def post_counter(id, lang):
    lang_code = Language.objects.get(code=lang.upper())
    d_post_lang_obj = DPostLang.objects.filter(post_id=id, lang_id=lang_code.id).first()
    d_post_lang_obj.view_count += 1
    d_post_lang_obj.save()


