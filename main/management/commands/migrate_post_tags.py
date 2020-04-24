from django.core.management.base import BaseCommand
from nodeads_libs.web_lib_core.models import PostTags, DPostTag, DPostTagLang
from django.db.models import Q


class Command(BaseCommand):

    help = 'Migrate PostTag model from old db'

    def handle(self, *args, **options):
        group_id_list = [1, 2, 3, 4]
        my_filter_qs = Q()
        for group_id in group_id_list:
            my_filter_qs = my_filter_qs | Q(groupid=group_id)
        post_tags_qs = PostTags.objects.filter(my_filter_qs)
        for post_tag in post_tags_qs:
            group_id = post_tag.groupid
            name = post_tag.name
            old_id = post_tag.id
            d_post_tag = DPostTag.objects.create(post_group_id=group_id, name=name, old_id=old_id)
            DPostTagLang.objects.create(name=name, lang_id=2, post_tag_id=d_post_tag.id)
        print('Migration finished')
