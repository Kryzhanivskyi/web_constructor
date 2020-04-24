import os

from django.db import models
from django.utils.safestring import mark_safe
from image_cropping import ImageRatioField
from PIL import Image
from .validators import validate_size


def type_based_upload_to(instance, filename):
    return f"content/items/{instance.type_name}/{filename}"


'''Abstract models    *********************************************************************** '''


class BaseGroupModel(models.Model):
    name = models.CharField(max_length=256,)
    order_index = models.PositiveSmallIntegerField(default=0)
    is_visible = models.BooleanField(default=False, blank=True)

    def max_filesize(self):
        self.file_limit = 1   # 1MB
        return self.file_limit

    class Meta:
        abstract = True


class BaseGroupLangModel(models.Model):
    lang = models.ForeignKey('Language', on_delete=models.PROTECT)
    name = models.CharField(max_length=256,)

    class Meta:
        abstract = True


class BaseContentModel(models.Model):
    type_name = 'none'
    url = models.FileField(blank=True, upload_to=type_based_upload_to, validators=[validate_size], max_length=1024)
    preview_url = models.FileField(blank=True, upload_to=type_based_upload_to, validators=[validate_size], max_length=1024)
    is_visible = models.BooleanField(default=False, blank=True)
    order_index = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    def max_filesize(self):
        self.file_limit = 1
        return self.file_limit

    class Meta:
        abstract = True


class BaseLangModel(models.Model):
    lang = models.ForeignKey('Language', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=1024,)

    class Meta:
        abstract = True


''' *********************************************************************** '''


class Language(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'languages'
        db_table = 'language'


'''Content    *********************************************************************** '''


class NonStrippingCharField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(NonStrippingCharField, self).formfield(**kwargs)


class ContentType(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    file_is_image = models.BooleanField(default=False)
    order_index = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'content_types'
        db_table = 'content_type'
        ordering = ('order_index',)


class Content(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_single_lang = models.BooleanField(default=False, blank=True)
    is_visible = models.BooleanField(default=True, blank=True)
    html = models.TextField(null=True, blank=True)
    html_item = NonStrippingCharField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'contents'
        db_table = 'content'


class Page(models.Model):
    root_content = models.ForeignKey(Content, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=120)
    url = models.CharField(blank=True, max_length=250)
    is_reg_exp = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'pages'
        db_table = 'page'


class PageParam(models.Model):
    page = models.ForeignKey(Page, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=120)
    value = models.CharField(max_length=120, null=True, blank=True)
    is_reg_exp = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'page_params'
        db_table = 'page_param'


class PageLang(models.Model):
    page = models.ForeignKey(Page, on_delete=models.PROTECT, null=True)
    lang = models.ForeignKey(Language, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    keywords = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        default_related_name = 'page_langs'
        db_table = 'page_lang'


class ContentLang(models.Model):
    content = models.ForeignKey(Content, null=True, on_delete=models.PROTECT)
    lang = models.ForeignKey(Language, null=True, on_delete=models.PROTECT)
    is_visible = models.BooleanField(default=True, blank=True)
    html = models.TextField(null=True, blank=True)
    html_item = NonStrippingCharField(null=True, blank=True)

    def __str__(self):
        return self.content.name

    class Meta:
        default_related_name = 'content_langs'
        db_table = 'content_lang'


class ContentItem(models.Model):
    content = models.ForeignKey(Content, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    html = models.TextField(null=True, blank=True)
    file_url = models.FileField(blank=True, upload_to='content/items/file_url')
    url = models.CharField(blank=True, max_length=250)
    inner_url = models.TextField(null=True, blank=True)
    order_index = models.PositiveIntegerField(blank=True, default=0)
    is_single_lang = models.BooleanField(default=False, blank=True)
    is_visible = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name

    # @property
    # def lang_list(self):
    #     return list(self.content_item_langs.all().values_list('lang__code', flat=True))
    #
    # @property
    # def content_type(self):
    #     return self.content.content_type.name

    class Meta:
        default_related_name = 'content_items'
        db_table = 'content_item'
        ordering = ('order_index',)


class ContentItemLang(models.Model):
    content_item = models.ForeignKey(ContentItem, null=True, on_delete=models.PROTECT)
    lang = models.ForeignKey(Language, null=True, on_delete=models.PROTECT)
    name = models.CharField(blank=True, max_length=250)
    html = models.TextField(null=True, blank=True)
    file_url = models.FileField(blank=True, upload_to='content/items/lang/file_url')
    url = models.CharField(blank=True, max_length=250)
    inner_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.content_item.name

    class Meta:
        unique_together = ("content_item", "lang")
        default_related_name = 'content_item_langs'
        db_table = 'content_item_lang'


''' *********************************************************************** '''


class DImageGroup(BaseGroupModel):
    preview_url = models.ImageField(null=True, blank=True, validators=[validate_size],
                                    upload_to='content/items/group_prev/images')
    cropping = ImageRatioField('preview_url', '40x40', size_warning=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id and os.path.exists(self.preview_url.path):  # check if update not create
            this = DImageGroup.objects.get(id=self.id)  # old object
            if this.cropping != self.cropping:
                original_image = Image.open(self.preview_url.path)
                cropping_coordinates = [int(c) for c in self.cropping.split(',')]
                cropping_image = original_image.crop(cropping_coordinates)
                cropping_image.save(self.preview_url.path)

        super(DImageGroup, self).save()

    def preview(self):
        return mark_safe(u'<img style="height:100px;" src="%s" />' % (self.preview_url.url if self.preview_url else ''))

    def image_link(self):
        return mark_safe(u'<a href="%s">Link</a>' % (self.preview_url.url if self.preview_url else ''))

    preview.short_description = 'Preview'
    image_link.short_description = 'Link'
    preview.allow_tags = True

    class Meta:
        default_related_name = 'd_image_groups'
        db_table = 'd_image_group'


class DVideoGroup(BaseGroupModel):
    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'd_video_groups'
        db_table = 'd_video_group'


class DMusicGroup(BaseGroupModel):
    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'd_music_groups'
        db_table = 'd_music_group'


class DImageGroupLang(BaseGroupLangModel):
    image_group = models.ForeignKey(DImageGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.image_group.name

    class Meta:
        default_related_name = 'd_image_group_langs'
        db_table = 'd_image_group_lang'


class DVideoGroupLang(BaseGroupLangModel):
    video_group = models.ForeignKey(DVideoGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.video_group.name

    class Meta:
        default_related_name = 'd_video_group_langs'
        db_table = 'd_video_group_lang'


class DMusicGroupLang(BaseGroupLangModel):
    music_group = models.ForeignKey(DMusicGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.music_group.name

    class Meta:
        default_related_name = 'd_music_group_langs'
        db_table = 'd_music_group_lang'


class DImage(BaseContentModel):
    type_name = 'images'
    image_group = models.ForeignKey(DImageGroup, on_delete=models.PROTECT, )

    def __str__(self):
        return self.image_group.name

    class Meta:
        default_related_name = 'd_images'
        db_table = 'd_image'


class DVideo(BaseContentModel):
    type_name = 'videos'
    video_group = models.ForeignKey(DVideoGroup, on_delete=models.PROTECT, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def max_filesize(self):
        self.file_limit = 50  #50MB
        return self.file_limit

    class Meta:
        default_related_name = 'd_videos'
        db_table = 'd_video'


class DVideoTag(models.Model):
    video_group = models.ForeignKey(DVideoGroup, on_delete=models.PROTECT)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'd_video_tags'
        db_table = 'd_video_tag'


class DVideoTagLink(models.Model):
    tag = models.ForeignKey(DVideoTag, on_delete=models.PROTECT)
    video = models.ForeignKey(DVideo, on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'd_video_tag_links'
        db_table = 'd_video_tag_link'


class DVideoTagLang(BaseLangModel):
    video_tag = models.ForeignKey(DVideoTag, on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'd_video_tag_langs'
        db_table = 'd_video_tag_lang'


class DMusic(BaseContentModel):
    type_name = 'music'
    music_group = models.ForeignKey(DMusicGroup, on_delete=models.PROTECT)
    minus_url = models.CharField(blank=True, max_length=250)
    video_url = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return self.music_group.name

    def max_filesize(self):
        self.file_limit = 10   #10MB
        return self.file_limit

    class Meta:
        default_related_name = 'd_musics'
        db_table = 'd_music'


class DImageLang(BaseLangModel):
    image = models.ForeignKey(DImage, on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'd_image_langs'
        db_table = 'd_image_lang'


class DVideoLang(BaseLangModel):
    video = models.ForeignKey(DVideo, on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'd_video_langs'
        db_table = 'd_video_lang'


class DMusicLang(BaseLangModel):
    music = models.ForeignKey(DMusic, on_delete=models.PROTECT)
    singer = models.CharField(max_length=64, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    accord = models.TextField(null=True, blank=True)

    class Meta:
        default_related_name = 'd_music_langs'
        db_table = 'd_music_lang'


'''  Posts ***********************************************************************  '''


class DPostGroup(BaseGroupModel):
    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'd_post_groups'
        db_table = 'd_post_group'


class DPostGroupLang(BaseGroupLangModel):
    post_group = models.ForeignKey(DPostGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.post_group.name

    class Meta:
        default_related_name = 'd_post_group_langs'
        db_table = 'd_post_group_lang'


class DPostTag(models.Model):
    post_group = models.ForeignKey(DPostGroup, on_delete=models.PROTECT)
    name = models.CharField(max_length=256, null=True)
    old_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'd_post_tags'
        db_table = 'd_post_tag'


class DPostTagLink(models.Model):
    tag = models.ForeignKey(DPostTag, on_delete=models.PROTECT)
    post = models.ForeignKey('DPost', on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'd_post_tag_links'
        db_table = 'd_post_tag_link'


class DPostTagLang(BaseLangModel):
    post_tag = models.ForeignKey(DPostTag, on_delete=models.PROTECT)

    class Meta:
        default_related_name = 'd_post_tag_langs'
        db_table = 'd_post_tag_lang'


class DPost(BaseContentModel):
    type_name = 'post'
    name = models.CharField(max_length=1024, blank=True)
    description = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = 'd_posts'
        db_table = 'd_post'


class DPostLang(BaseLangModel):
    post = models.ForeignKey(DPost, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    full_text = models.TextField()
    keywords = models.CharField(max_length=1024, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)

    class Meta:
        default_related_name = 'd_post_langs'
        db_table = 'd_post_lang'


class DPostVideo(models.Model):
    post = models.ForeignKey(DPost, on_delete=models.PROTECT)
    youtube_code = models.CharField(max_length=64)
    is_visible = models.BooleanField(default=True, blank=True)
    order_index = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.post.name

    class Meta:
        default_related_name = 'd_post_videos'
        db_table = 'd_post_video'


class DPostImage(models.Model):
    post = models.ForeignKey(DPost, on_delete=models.PROTECT)
    image = models.ImageField(null=True, blank=True, validators=[validate_size],
                              upload_to='content/items/post_images')
    cropping = ImageRatioField('image', '600x300')
    is_visible = models.BooleanField(default=True, blank=True)
    order_index = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'P:{self.post.name}, I:{self.image if self.image else "<empty>"}'

    def max_filesize(self):
        self.file_limit = 1
        return self.file_limit

    def save(self, *args, **kwargs):
        if self.id and os.path.exists(self.image.path):  # check if update not create
            this = DPostImage.objects.get(id=self.id)  # old object
            if this.cropping != self.cropping:
                original_image = Image.open(self.image.path)
                cropping_coordinates = [int(c) for c in self.cropping.split(',')]
                cropping_image = original_image.crop(cropping_coordinates)
                cropping_image.save(self.image.path)

        super(DPostImage, self).save()

    def preview(self):
        return mark_safe(u'<img style="height:100px;" src="%s" />' % (self.image.url if self.image else ''))

    def image_link(self):
        return mark_safe(u'<a href="%s">Link</a>' % (self.image.url if self.image else ''))
    
    preview.short_description = 'Preview'
    image_link.short_description = 'Link'
    preview.allow_tags = True

    class Meta:
        default_related_name = 'd_post_images'
        db_table = 'd_post_image'




'''  Translation Text ***********************************************************************  '''


class TranslationText(models.Model):
    text_code = models.CharField(max_length=250, verbose_name='Ідентифікатор тексту', help_text="Коротке значення",
                                 unique=True, )
    EN = models.TextField(verbose_name='Англійською', blank=True, default='')
    RU = models.TextField(verbose_name='Російською', blank=True, default='')
    UA = models.TextField(verbose_name='Українською', blank=True, default='')
    DE = models.TextField(verbose_name='Німецькою', blank=True, default='')

    def __str__(self):
        return self.text_code

    @property
    def text_dict(self):
        return {self.text_code: {'EN': self.EN, 'RU': self.RU, 'UA': self.UA, 'DE': self.DE}}

    @property
    def page_count(self):
        return self.page_texts.count()

    class Meta:
        db_table = 'translation_text'


class TranslationPage(models.Model):
    name = models.CharField(verbose_name="Ім'я сторінки", blank=True, max_length=200)
    code = models.CharField(verbose_name="Код", max_length=200, unique=True, default='')
    template_name = models.CharField(verbose_name='Назва файлу', max_length=200, default='')

    def __str__(self):
        return self.name if self.name else self.code

    class Meta:
        db_table = 'translation_page'
        ordering = ('id',)


class TranslationPageText(models.Model):
    page = models.OneToOneField(TranslationPage, verbose_name='Сторінка', on_delete=models.CASCADE)
    texts = models.ManyToManyField(TranslationText, verbose_name="Слова, прив'язані до сторінки")

    def __str__(self):
        return 'Html: %s' % self.page

    @property
    def texts_list(self):
        return list(self.texts.all())

    @property
    def texts_count(self):
        return self.texts.count()

    class Meta:
        default_related_name = 'page_texts'
        db_table = 'translation_page_text'


''' OLD VOORG MODELS   ***********************************************************************  '''


class PostTags(models.Model):
    groupid = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    url = models.CharField(max_length=64, blank=True, null=True)
    sitemapenable = models.SmallIntegerField(blank=True, null=True)
    apiappexpose = models.SmallIntegerField()
    urlprefix = models.CharField(max_length=256, blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_tags'


class Posts(models.Model):
    url = models.CharField(max_length=1024, blank=True, null=True)
    description = models.CharField(max_length=4096, blank=True, null=True)
    keywords = models.CharField(max_length=4096, blank=True, null=True)
    pagetitle = models.CharField(max_length=4096)
    imageid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True)
    titleen = models.CharField(max_length=512, blank=True, null=True)
    fulltext = models.TextField(blank=True, null=True)
    fulltexten = models.TextField(blank=True, null=True)
    previewtext = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)
    authorid = models.IntegerField(blank=True, null=True)
    lastmodifier = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    deleted = models.IntegerField()
    charity = models.SmallIntegerField()
    youtube = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'posts'


class PostTagLink(models.Model):
    tagid = models.IntegerField(blank=True, null=True)
    postid = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_tag_link'


class PostVideoLink(models.Model):
    videoid = models.IntegerField(blank=True, null=True)
    postid = models.IntegerField(blank=True, null=True)
    youtubecode = models.CharField(max_length=64)
    position = models.IntegerField(blank=True, null=True)
    small = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_video_link'


class PostImageLink(models.Model):
    imageid = models.IntegerField(blank=True, null=True)
    postid = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_image_link'


class Images(models.Model):
    serverid = models.IntegerField(blank=True, null=True)
    dir = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    typeid = models.IntegerField(blank=True, null=True)
    hash = models.CharField(max_length=32, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True)
    alt = models.CharField(max_length=512, blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)
    authorid = models.IntegerField(blank=True, null=True)
    lastmodifier = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class VideoTagGroups(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'video_tag_groups'


class Videos(models.Model):
    serviceid = models.IntegerField(blank=True, null=True)
    serverid = models.CharField(max_length=32, blank=True, null=True)
    serveriden = models.CharField(max_length=32, blank=True, null=True)
    imageid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    titleen = models.CharField(max_length=256, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    authorid = models.IntegerField(blank=True, null=True)
    lastmodifier = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videos'
