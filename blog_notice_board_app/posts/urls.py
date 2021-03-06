from django.conf.urls import url
from posts import views

# these are thebiuld in views used for authentication,
# we use it only for password change
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),

    # url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^categories/$', views.all_categories, name='all_categories'),

    url(r'^$', views.login, name='homepage'),
    # url(r'^login/$', views.login, name='login'),
    url(r'^list/$', views.post_list, name="list"),
    url(r'^create/$', views.post_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
]
