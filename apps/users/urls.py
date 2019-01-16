from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^usernames/(?P<username>[\s\S]{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^invite/num/(?P<invite_num_son>\d{5,20})/count/$', views.InviteNumCountView.as_view()),
    url(r'^purse/addr/(?P<purse_addr>0x[a-zA-Z0-9]{40})/count/$', views.PurseAddrCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^users/$', views.UserView.as_view()),
    url(r'^authorizations/$', views.UserAuthentication.as_view()),
    url(r'^user/$', views.UserDetailView.as_view()),
    url(r'^member/$', views.MemberDetailView.as_view()),
    url(r'^search/$', views.SearchUserView.as_view()),
    url(r'^grant/$', views.GrantUserView.as_view()),
    url(r'^rsearch/$', views.GrantSearchView.as_view()),
    url(r'^member/user/$', views.MemberUserView.as_view()),
    url(r'^node/vip/$', views.VIPNodeView.as_view()),
    url(r'^node/mem/$', views.MemNodeView.as_view()),
    url(r'^node/fans/$', views.FansNodeView.as_view()),
    url(r'^node/search/$', views.SearchNodeView.as_view()),
    url(r'^modify/$', views.ModifyView.as_view()),
    url(r'^export/$', views.ExportView.as_view())
]