from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .forms import ContentItemLangAdminForm
from .models import (ContentLang, ContentItemLang, DImageGroupLang, DVideoGroupLang, DMusicGroupLang, DPostGroupLang,
                     DImageLang, DVideoLang, DMusicLang, DPostLang, PageLang, DPostTagLang, DPostImage, DPostVideo,
                     PageParam, DVideoTagLang)


class ContentItemLangInLine(admin.TabularInline):
    model = ContentItemLang
    form = ContentItemLangAdminForm
    extra = 3


class ContentLangInLine(admin.TabularInline):
    model = ContentLang
    extra = 3


class PageLangInLine(admin.TabularInline):
    model = PageLang
    extra = 3


class DImageGroupLangInLine(admin.TabularInline):
    model = DImageGroupLang
    extra = 3


class DVideoGroupLangInLine(admin.TabularInline):
    model = DVideoGroupLang
    extra = 3


class DMusicGroupLangInLine(admin.TabularInline):
    model = DMusicGroupLang
    extra = 3


class DPostGroupLangInLine(admin.TabularInline):
    model = DPostGroupLang
    extra = 3


class DImageLangInLine(admin.TabularInline):
    model = DImageLang
    extra = 3


class DVideoLangInLine(admin.TabularInline):
    model = DVideoLang
    extra = 3


class DMusicLangInLine(admin.TabularInline):
    model = DMusicLang
    extra = 3


class DPostLangInLine(admin.TabularInline):
    model = DPostLang
    extra = 3


class DPostTagLangInLine(admin.TabularInline):
    model = DPostTagLang
    extra = 3


class DPostImageInLine(admin.TabularInline):
    model = DPostImage
    extra = 1
    fields = ('image', 'preview', 'is_visible', 'order_index', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'preview')


class DPostVideoInLine(admin.TabularInline):
    model = DPostVideo
    extra = 1


class PageParamInLine(admin.TabularInline):
    model = PageParam
    extra = 1


class DVideoTagLangInLine(admin.TabularInline):
    model = DVideoTagLang
    extra = 1
