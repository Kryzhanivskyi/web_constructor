from django.apps import AppConfig


class WebLibMultiLanguageConfig(AppConfig):
    name = 'nodeads_libs.web_lib_core'
    verbose_name = "Lib Ui"

    def ready(self):
        import nodeads_libs.web_lib_core.signals