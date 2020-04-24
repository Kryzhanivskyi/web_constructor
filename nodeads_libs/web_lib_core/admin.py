from django.contrib import admin
from image_cropping import ImageCroppingMixin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .inlines import (ContentItemLangInLine, PageLangInLine, ContentLangInLine,
                      DImageGroupLangInLine, DVideoGroupLangInLine, DMusicGroupLangInLine, DPostGroupLangInLine,
                      DImageLangInLine, DMusicLangInLine, DVideoLangInLine, DPostLangInLine, DPostTagLangInLine,
                      DPostImageInLine, DPostVideoInLine, PageParamInLine, DVideoTagLangInLine)
from .models import (Language, TranslationText, TranslationPageText, TranslationPage, ContentType, Content, Page,
                     ContentItem,  DImageGroup, DVideoGroup, DPostGroup, DMusicGroup, DImage, DVideo, DMusic, DPost,
                     PageParam, DPostTag, DPostTagLink, DPostImage, DPostVideo, DVideoTag, DVideoTagLink)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = ('code', 'name')
    list_display = ('id', 'code', 'name')


'''Content    *********************************************************************** '''


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'file_is_image', 'order_index')
    list_display = ('id', 'name', 'description', 'file_is_image', 'order_index')
    list_filter = ('name', 'order_index')
    search_fields = ('name',)
    list_display_links = ('id',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    fields = ('name', 'content_type', 'description', 'is_single_lang', 'is_visible', 'html', 'html_item', 'created',
              'updated')
    list_display = ('id', 'name', 'content_type', 'description', 'is_single_lang', 'is_visible', 'html', 'html_item',
                    'created', 'updated')
    list_filter = ('content_type', 'is_single_lang', 'is_visible')
    search_fields = ('name', 'html', 'html_item')
    list_display_links = ('id',)
    readonly_fields = ('created', 'updated')
    raw_id_fields = ('content_type',)
    inlines = [ContentLangInLine]


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    fields = ('name', 'content', 'html', 'file_url', 'url', 'inner_url', 'order_index', 'is_single_lang', 'is_visible')
    list_display = ('id', 'name', 'content', 'file_url', 'url', 'inner_url', 'order_index', 'is_single_lang',
                    'is_visible')
    list_filter = ('order_index', 'is_visible')
    search_fields = ('name', 'content')
    raw_id_fields = ('content',)
    inlines = [ContentItemLangInLine]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fields = ('name', 'root_content', 'url', 'is_reg_exp', 'created', 'updated')
    list_display = ('id', 'name', 'get_content_type', 'root_content', 'url', 'is_reg_exp', 'created', 'updated')
    list_filter = ('root_content',)
    search_fields = ('name',)
    raw_id_fields = ('root_content',)
    readonly_fields = ('created', 'updated')
    inlines = [PageLangInLine, PageParamInLine]

    def get_content_type(self, obj):
        return obj.root_content.content_type

    get_content_type.admin_order_field = 'content_type'
    get_content_type.short_description = 'content type'


@admin.register(PageParam)
class PageParamAdmin(admin.ModelAdmin):
    fields = ('page', 'name', 'value', 'is_reg_exp', 'created', 'updated')
    list_display = ('id', 'page', 'name', 'value', 'is_reg_exp', 'created', 'updated')
    list_filter = ('is_reg_exp',)
    search_fields = ('name', 'page')
    list_display_links = ('id',)
    readonly_fields = ('created', 'updated')
    raw_id_fields = ('page',)


''' *********************************************************************** '''


@admin.register(DImageGroup)
class DImageGroupAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = ('name', 'preview_url', 'cropping', 'order_index', 'is_visible')
    list_display = ('id', 'name', 'image_link', 'preview', 'order_index', 'is_visible')
    search_fields = ('name',)
    list_display_links = ('id',)
    inlines = [DImageGroupLangInLine]


@admin.register(DVideoGroup)
class DVideoGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'order_index', 'is_visible')
    list_display = ('id', 'name', 'order_index', 'is_visible')
    search_fields = ('name',)
    list_display_links = ('id',)
    inlines = [DVideoGroupLangInLine]


@admin.register(DMusicGroup)
class DMusicGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'order_index', 'is_visible')
    list_display = ('id', 'name', 'order_index', 'is_visible')
    search_fields = ('name',)
    list_display_links = ('id',)
    inlines = [DMusicGroupLangInLine]


@admin.register(DPostGroup)
class DPostGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'order_index', 'is_visible')
    list_display = ('id', 'name', 'order_index', 'is_visible')
    search_fields = ('name',)
    list_display_links = ('id',)
    inlines = [DPostGroupLangInLine]


''' *********************************************************************** '''


@admin.register(DImage)
class DImageAdmin(admin.ModelAdmin):
    fields = ('image_group', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_display = ('id', 'image_group', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_filter = ('is_visible',)
    search_fields = ('id', 'url', 'order_index')
    list_display_links = ('id',)
    readonly_fields = ('created', 'updated')
    raw_id_fields = ('image_group',)
    inlines = [DImageLangInLine]


@admin.register(DVideo)
class DVideoAdmin(admin.ModelAdmin):
    fields = ('video_group', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_display = ('id', 'video_group', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_filter = ('is_visible',)
    search_fields = ('id', 'url', 'order_index')
    list_display_links = ('id',)
    readonly_fields = ('created', 'updated')
    raw_id_fields = ('video_group',)
    inlines = [DVideoLangInLine]


@admin.register(DMusic)
class DMusicAdmin(admin.ModelAdmin):
    fields = ('music_group', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_display = ('id', 'music_group', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_filter = ('is_visible',)
    search_fields = ('id', 'url', 'order_index')
    list_display_links = ('id',)
    readonly_fields = ('created', 'updated')
    raw_id_fields = ('music_group',)
    inlines = [DMusicLangInLine]


@admin.register(DPost)
class DPostAdmin(admin.ModelAdmin):
    fields = ('url', 'name', 'preview_url', 'description', 'full_text', 'is_visible', 'order_index', 'created', 'updated')
    list_display = ('id', 'url', 'preview_url', 'is_visible', 'order_index', 'created', 'updated')
    list_filter = ('is_visible',)
    search_fields = ('id', 'url', 'order_index')
    list_display_links = ('id',)
    readonly_fields = ('created', 'updated')
    inlines = [DPostLangInLine, DPostImageInLine, DPostVideoInLine]


'''  Tags *********************************************************************** '''


@admin.register(DPostTag)
class DPostTagAdmin(admin.ModelAdmin):
    fields = ('post_group', 'name')
    list_display = ('id', 'post_group', 'name')
    search_fields = ('name',)
    list_display_links = ('id',)
    raw_id_fields = ('post_group',)
    inlines = [DPostTagLangInLine]


@admin.register(DPostTagLink)
class DPostTagLinkAdmin(admin.ModelAdmin):
    fields = ('tag', 'post')
    list_display = ('id', 'tag', 'post')
    search_fields = ('tag',)
    list_display_links = ('id',)
    raw_id_fields = ('tag', 'post')


@admin.register(DVideoTag)
class DVideoTagAdmin(admin.ModelAdmin):
    fields = ('video_group', 'name')
    list_display = ('id', 'video_group', 'name')
    search_fields = ('name',)
    list_display_links = ('id',)
    raw_id_fields = ('video_group',)
    inlines = [DVideoTagLangInLine]


@admin.register(DVideoTagLink)
class DVideoTagLinkAdmin(admin.ModelAdmin):
    fields = ('tag', 'video')
    list_display = ('id', 'tag', 'video')
    search_fields = ('tag',)
    list_display_links = ('id',)
    raw_id_fields = ('tag', 'video')


''' Post Video  ***********************************************************************  '''


@admin.register(DPostVideo)
class DPostVideoAdmin(admin.ModelAdmin):
    fields = ('post', 'youtube_code', 'is_visible', 'order_index', 'created', 'updated')
    list_display = ('id', 'post', 'youtube_code', 'is_visible', 'order_index', 'created', 'updated')
    search_fields = ('youtube_code', 'order_index')
    list_filter = ('is_visible',)
    list_display_links = ('id',)
    raw_id_fields = ('post',)
    readonly_fields = ('created', 'updated')


'''  Post Image ***********************************************************************  '''


@admin.register(DPostImage)
class DPostImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = ('post', 'image', 'cropping', 'is_visible', 'order_index', 'created', 'updated')
    list_display = ('id', 'post', 'image_link', 'preview', 'is_visible', 'order_index', 'created', 'updated')
    search_fields = ('order_index',)
    list_filter = ('is_visible',)
    list_display_links = ('id',)
    raw_id_fields = ('post',)
    readonly_fields = ('created', 'updated')


'''  Translation Text ***********************************************************************  '''


@admin.register(TranslationPage)
class TranslationPageAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'code',  'template_name')
    list_display = ('id', 'name', 'code',  'template_name')
    readonly_fields = ('id',)
    list_display_links = ('id', 'name')
    search_fields = ('name', 'code',)


@admin.register(TranslationText)
class TranslationTextAdmin(admin.ModelAdmin):
    fields = ('id', 'text_code', 'EN', 'RU', 'UA', 'DE',  'page_count')
    list_display = ('id', 'text_code', 'EN', 'RU', 'UA', 'DE',  'get_page_count')
    readonly_fields = ('id', 'page_count')
    search_fields = ('text_code', 'EN', 'RU', 'UA', 'DE',)
    list_filter = ('page_texts', )

    def get_page_count(self, obj):
        return obj.page_count

    get_page_count.short_description = 'Кількість сторінок'


@admin.register(TranslationPageText)
class TranslationPageAdmin(admin.ModelAdmin):
    fields = ('page', 'texts', 'texts_count')
    list_display = ('page', 'get_texts_count', 'get_texts_list')
    raw_id_fields = ('page',)
    filter_horizontal = ('texts',)
    readonly_fields = ('texts_count', )
    search_fields = ('texts__text_code',)

    def get_texts_count(self, obj):
        return obj.texts_count

    get_texts_count.short_description = 'Кількість'

    def get_texts_list(self, obj):
        return obj.texts_list

    get_texts_list.short_description = "Слова, прив'язані до сторінки"


'''   *********************************************************************** '''
