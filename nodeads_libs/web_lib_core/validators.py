from django.core.exceptions import ValidationError


def validate_size(value):
    file_size = value.size
    megabyte_limit = value.instance.max_filesize()
    if file_size > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))





