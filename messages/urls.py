from django.conf.urls import url
from django.urls import re_path

from . import views

app_name = "messages"

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^(?P<message_id>\d+)/$', views.detail, name='detail'),
    re_path(r'signup', views.signup, name='signup')
]
