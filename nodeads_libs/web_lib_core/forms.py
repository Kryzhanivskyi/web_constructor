from django import forms
from .models import ContentItemLang


class ContentItemLangAdminForm(forms.ModelForm):
    # html = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = ContentItemLang
        fields = '__all__'



