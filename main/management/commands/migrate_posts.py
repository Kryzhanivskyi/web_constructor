from django.core.management.base import BaseCommand
from nodeads_libs.web_lib_core.models import DPostTag, PostTagLink, Posts, DPost, DPostLang, PostVideoLink, DPostVideo,\
    Images, PostImageLink, DPostImage
from django.db.models import Q
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class Command(BaseCommand):

    help = 'Migrate Posts model from old db'

    def handle(self, *args, **options):
        old_id_qs = DPostTag.objects.values_list('old_id')
        old_ids = list()
        post_ids = list()
        for old_id in old_id_qs:
            old_ids.append(old_id[0])
        my_filter_qs = Q()
        for id in old_ids:
            my_filter_qs = my_filter_qs | Q(tagid=id)
        post_tag_link_qs = PostTagLink.objects.filter(my_filter_qs).distinct('postid')
        for id in post_tag_link_qs.values_list('id'):
            post_ids.append(id[0])
        post_filter_qs = Q()
        for id in post_ids:
            post_filter_qs = post_filter_qs | Q(id=id)
        posts_qs = Posts.objects.filter(post_filter_qs)
        for post in posts_qs:
            post_url = post.url
            post_name = post.title
            post_description = post.description
            post_keywords = post.keywords
            post_image_id = post.imageid
            post_full_text = post.fulltext.replace(r'\r', "\r").replace(r'\n', "\n")
            post_deleted = post.deleted
            post_created = post.created
            post_updated = post.modified
            d_post_where = {'url': post_url, 'created': post_created, 'name': post_name,
                            'description': post_description, 'full_text': post_full_text}
            if post_deleted == 0:
                d_post_where['is_visible'] = True
            if post_updated is not None:
                d_post_where['updated'] = post_updated
            else:
                d_post_where['updated'] = post_created
            d_post = DPost.objects.create(**d_post_where)
            d_post.order_index = (d_post.id * 10)
            if post_image_id:
                preview_image = Images.objects.get(pk=post_image_id)
                preview_image_name = preview_image.name
                preview_image_dir = preview_image.dir
                preview_image_link = 'http://st0.vo.org.ua/images/' + f'{preview_image_dir}' + '/sp_'+ f'{preview_image_name}' +'.jpg'
                r = requests.get(preview_image_link)
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(r.content)
                img_temp.flush()
                d_post.preview_url.save(preview_image_name + '.jpg', File(img_temp), save=True)
            d_post.save()
            d_post_lang_where = {'name': post_name, 'description': post_description, 'keywords': post_keywords,
                                 'lang_id': 2, 'post_id': d_post.id, 'full_text': post_full_text, 'created': post_created}
            if post_updated is not None:
                d_post_lang_where['updated'] = post_updated
            else:
                d_post_lang_where['updated'] = post_created
            DPostLang.objects.create(**d_post_lang_where)
            post_video_link_qs = PostVideoLink.objects.filter(postid=post.id)
            if post_video_link_qs:
                for post_video in post_video_link_qs:
                    d_post_video = DPostVideo.objects.create(youtube_code=post_video.youtubecode, post_id=d_post.id)
                    d_post_video.order_index = (d_post_video.id * 10)
                    d_post_video.save()
            post_image_link_qs = PostImageLink.objects.filter(postid=post.id)
            if post_image_link_qs:
                for post_image in post_image_link_qs:
                    image_id = post_image.imageid
                    image = Images.objects.get(pk=image_id)
                    image_name = image.name
                    image_dir = image.dir
                    image_link = 'http://st0.vo.org.ua/images/' + f'{image_dir}' + '/v_' + f'{image_name}' + '.jpg'
                    req = requests.get(image_link)
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(req.content)
                    img_temp.flush()
                    d_post_image = DPostImage.objects.create(post_id=d_post.id)
                    d_post_image.image.save(image_name + '.jpg', File(img_temp), save=True)
                    d_post_image.order_index = (d_post_image.id * 10)
                    d_post_image.save()
        print('Migration finished')




