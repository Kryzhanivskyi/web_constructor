import codecs
import re

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import get_object_or_404

from .models import TranslationPageText, TranslationText, Page, ContentItemLang


def translation_page_text(code, language='RU'):
    try:
        TranslationText._meta.get_field(str(language).upper())
    except FieldDoesNotExist:
        language = 'RU'
    page_text_dict = {}
    texts = TranslationPageText.objects.filter(page__code=code).first()
    texts = texts.texts_list if texts else []
    for text in texts:
        for key, value in text.text_dict.items():
            page_text_dict[key] = value[language.upper()] if value else key
    return page_text_dict


def lack_of_tr_word_list(template):
    html = codecs.open(settings.BASE_DIR + '/templates/' + template, 'r', "utf_8_sig")
    html_text = html.read()
    text_list = re.findall(r'\%(\w+)\%', html_text)
    extends = re.findall(r"\{\% extends \'(\w.+)\' \%\}", html_text)
    include_list = re.findall(r"\{\% include \'(\w.+)\' \%\}", html_text)
    html.close()
    if extends:
        extends_dict = lack_of_tr_word_list(extends[0])
        text_list.extend(list(extends_dict[extends[0]]['text_set']))
    if include_list:
        for page in include_list:
            include_dict = lack_of_tr_word_list(page)
            text_list.extend(list(include_dict[page]['text_set']))
    return {template: {'text_set': set(text_list), 'extends': extends, 'include': include_list}}


def parse_html(html, item_queryset):
    item_list = re.findall(r'\{item\.\d+\}', html)
    for item in item_list:
        item_id = int(item.replace('}', '').replace('{item.', ''))
        html = html.replace(item, item_queryset.get(content_item_id=item_id).html)
    check_list = re.findall(r'\{item\.\d+\}', html)
    if check_list:
        html = parse_html(html, item_queryset)

    return html


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def fill_by_loop(template_text, queryset):
    name_loop_list = re.findall(r'\#(\w+)\#', template_text)
    for name_loop in name_loop_list:
        loop_matrix = queryset.filter(ui_item__name='{}_matrix'.format(name_loop),
                                      ui_item__ui__name='matrix').first().html
        loop_elements = queryset.filter(ui_item__ui__name='{}_element'.format(name_loop))
        loop_text = ''
        for element in loop_elements:
            loop_text += loop_matrix.replace('*URL*', element.url).replace('*NAME*', element.html)

        template_text = template_text.replace('#{}#'.format(name_loop), loop_text)
    return template_text


def fill_html(template_text, all_items_list, item_name='item'):
    item_id_list = re.findall(r'\%{}.(\d+)\%'.format(item_name), template_text)
    print(item_id_list)
    print(item_name)
    print(all_items_list)
    for item_dict in all_items_list:
        item_id = str(item_dict['ui_item_id'])
        if item_id in item_id_list:
            template_text = template_text.replace('%{0}.{1}%'.format(item_name, item_id), item_dict['html'])
            item_id_list = list(filter(lambda a: a != item_id, item_id_list))  # Del all same id

    if not item_id_list:
        check_item_id_list = re.findall(r'\%{}.(\d+)\%'.format(item_name), template_text)
        template_text = fill_html(template_text, all_items_list) if check_item_id_list else template_text

    return template_text


def fill_manager(request, slug):
    page = get_object_or_404(Page, slug=slug)
    lang_code = request.GET.get('lang', request.COOKIES.get('lang'))
    lang_code = lang_code.upper() if lang_code else 'RU'
    ui_queryset = ContentItemLang.objects.filter(lang__code=lang_code)
    content_queryset = ContentItemLang.objects.filter(lang__code=lang_code)

    ui_template = ui_queryset.get(ui_item_id=page.root_item.id).html

    all_items_list = ui_queryset.values('ui_item_id', 'html')
    all_content_items_list = content_queryset.values('content_item_id', 'html')

    template_text = fill_html(ui_template, all_items_list, 'item')  # %item.1%
    template_text = fill_html(template_text, all_content_items_list, 'CONTENT_item')  # %CONTENT_item.1%
    template_text = fill_by_loop(template_text, ui_queryset)  # #menu#
    return template_text

