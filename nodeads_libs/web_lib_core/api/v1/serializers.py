from rest_framework import serializers
from nodeads_libs.web_lib_core.models import TranslationText, TranslationPage, TranslationPageText, Language


class TranslationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationText
        fields = ('id', 'text_code', 'RU', 'EN', 'UA', 'DE')


class TranslationPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationPage
        fields = ('id', 'name', 'code', 'template_name')


class TranslationPageTextSerializer(serializers.ModelSerializer):
    page = TranslationPageSerializer()
    texts = TranslationTextSerializer(read_only=True, many=True)

    class Meta:
        model = TranslationPageText
        fields = ('id', 'page', 'texts')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'code', 'is_default', 'is_visible', 'order_index', 'flag_image')
