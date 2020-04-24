import os
from django.dispatch import receiver
from .models import DImageGroup, DPostImage
from django.db.models.signals import pre_save, post_delete


@receiver(pre_save, sender=DPostImage)
@receiver(pre_save, sender=DImageGroup)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    if sender is DImageGroup:
        try:
            old_file = sender.objects.get(pk=instance.pk).preview_url
        except sender.DoesNotExist:
            return False

        new_file = instance.preview_url
        if old_file:
            if not old_file == new_file:
                if os.path.isfile(old_file.path + '.600x300_q85_detail_upscale.jpg'):
                    os.remove(old_file.path + '.600x300_q85_detail_upscale.jpg')

    if sender is DPostImage:
        try:
            old_file = sender.objects.get(pk=instance.pk).image
        except sender.DoesNotExist:
            return False

        new_file = instance.image
        if old_file:
            if not old_file == new_file:
                if os.path.isfile(old_file.path + '.600x300_q85_detail_upscale.jpg'):
                    os.remove(old_file.path + '.600x300_q85_detail_upscale.jpg')


@receiver(post_delete, sender=DPostImage)
@receiver(post_delete, sender=DImageGroup)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if sender is DImageGroup:
        if instance.preview_url:
            if os.path.isfile(instance.preview_url.path + '.600x300_q85_detail_upscale.jpg'):
                os.remove(instance.preview_url.path + '.600x300_q85_detail_upscale.jpg')

    if sender is DPostImage:
        if instance.image:
            if os.path.isfile(instance.image.path + '.600x300_q85_detail_upscale.jpg'):
                os.remove(instance.image.path + '.600x300_q85_detail_upscale.jpg')
