from django.core.management.base import BaseCommand
from nodeads_libs.web_lib_core.models import VideoTagGroups, DVideoGroup, DVideoGroupLang


class Command(BaseCommand):

    help = 'Migrate VideoTagGroups model from old db'

    def handle(self, *args, **options):
        video_tag_groups_qs = VideoTagGroups.objects.all()
        for video_tag_group in video_tag_groups_qs:
            name = video_tag_group.name
            d_video_group = DVideoGroup.objects.create(name=name, is_visible=True)
            d_video_group.order_index = (d_video_group.id * 10)
            d_video_group.save()
            DVideoGroupLang.objects.create(name=name, lang_id=2, video_group_id=d_video_group.id)
        print('Migration finished')