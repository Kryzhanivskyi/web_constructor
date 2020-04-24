from django.urls import path, include
from .views import set_language, matrix_to_html

urlpatterns = [
    path('api/', include('nodeads_libs.web_lib_core.api.v1.urls')),
    path('set_language/', set_language, name='set_language'),
    path('matrix_to_html/', matrix_to_html, name='matrix_to_html')
]