from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^slider_aliyun/(?P<session>[\s\S]*)/(?P<sig>[\s\S]*)/(?P<token>[\s\S]*)/(?P<scene>[\s\S]*)', views.SliderView.as_view()),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view())
]