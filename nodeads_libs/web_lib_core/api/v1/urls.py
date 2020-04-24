from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from .views import (TranslationPageTextViewSet, TranslationPageViewSet, TranslationTextViewSet,
                                            LanguageViewSet)

router = routers.DefaultRouter()
router.register('tr_text', TranslationTextViewSet, base_name='translation_text')
router.register('tr_page', TranslationPageViewSet, base_name='translation_page')
router.register('tr_page_texts', TranslationPageTextViewSet, base_name='translation_page_text')
router.register('language', LanguageViewSet, base_name='language')


schema_view = get_schema_view()

urlpatterns = [
    path('v1/', include(router.urls)),
    path('schema/', schema_view)
]