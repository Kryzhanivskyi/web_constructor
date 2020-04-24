import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import (TranslationPageTextSerializer, TranslationPageSerializer, TranslationTextSerializer,
                          LanguageSerializer)
from nodeads_libs.web_lib_core.models import TranslationText, TranslationPage, TranslationPageText, Language
from nodeads_libs.web_lib_core.utils import lack_of_tr_word_list


class TranslationTextViewSet(viewsets.ModelViewSet):
    queryset = TranslationText.objects.all()
    serializer_class = TranslationTextSerializer


class TranslationPageViewSet(viewsets.ModelViewSet):
    queryset = TranslationPage.objects.all()
    serializer_class = TranslationPageSerializer


class TranslationPageTextViewSet(viewsets.ModelViewSet):
    queryset = TranslationPageText.objects.all()
    serializer_class = TranslationPageTextSerializer

    @action(detail=False, methods=['get'])
    def text_check(self, request):
        text_dict = {}
        html_list = []
        for root, dirs, files in os.walk(settings.BASE_DIR+"/templates"):
            html_dict = {'dirictory': root.split('/')[-1], 'text_files': [f for f in files if f.endswith('.html')]}
            if html_dict['dirictory'] == 'templates':
                html_list.extend(html_dict['text_files'])
            else:
                for html in html_dict['text_files']:
                    html_list.append('{0}/{1}'.format(html_dict['dirictory'], html)) #content/video.html
        for html in html_list:
            text_dict.update(lack_of_tr_word_list(html)) #"registration/new_password.html": ["reg_placeholder_phone",]

        '''Create text'''
        all_text = []
        for key, value in text_dict.items():
            text_set = value['text_set']
            all_text.extend(list(text_set)) #only text for create
        all_text = list(set(all_text)-set(TranslationText.objects.values_list('text_code', flat=True)))
        TranslationText.objects.bulk_create(TranslationText(text_code=n) for n in all_text)

        '''Create page-text many to many'''
        for key, value in text_dict.items():
            text_set = value['text_set']
            page = TranslationPage.objects.filter(template_name=key).first()
            text_page_list = list(TranslationText.objects.filter(text_code__in=text_set).all())
            if page:
                obj, create = TranslationPageText.objects.get_or_create(page_id=page.id)
                obj.texts.add(*text_page_list)

        return Response({'success': True, 'text_dict': text_dict}, status=status.HTTP_200_OK)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

