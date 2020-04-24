from django.core.management.base import BaseCommand
from nodeads_libs.web_lib_core.models import Videos, DVideo, DVideoLang, Images
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class Command(BaseCommand):

    help = 'Migrate VideoTagGroups model from old db'

    def handle(self, *args, **options):
        video_qs = Videos.objects.all()
        for video in video_qs:
            url = video.serverid
            name = video.title
            created = video.created
            updated = video.modified
            view_count = video.views
            image_id = video.imageid
            if not url or image_id == 0:
                continue
            d_video_where = {'url': url, 'view_count': view_count, 'created': created, 'is_visible': True}
            if updated is not None:
                d_video_where['updated'] = updated
            else:
                d_video_where['updated'] = created
            preview_image = Images.objects.filter(pk=image_id).first()
            if not preview_image:
                continue
            preview_image_name = preview_image.name
            preview_image_dir = preview_image.dir
            preview_image_link = 'http://st0.vo.org.ua/images/' + f'{preview_image_dir}' + '/sp_' + f'{preview_image_name}' + '.jpg'
            r = requests.get(preview_image_link)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush()
            d_video = DVideo.objects.create(**d_video_where)
            d_video.preview_url.save(preview_image_name + '.jpg', File(img_temp), save=True)
            d_video.order_index = (d_video.id * 10)
            d_video.save()
            DVideoLang.objects.create(video_id=d_video.id, name=name, lang_id=2)
        print('Migration finished')
