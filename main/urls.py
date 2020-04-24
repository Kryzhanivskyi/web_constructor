from django.urls import path
from main import views


urlpatterns = [
    path('', views.main, name='main'),
    path('<path:slug>', views.slug_main, name='slug_main')
]
