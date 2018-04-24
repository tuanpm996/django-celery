from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(
        r'(?P<fanpage_id>[0-9|a-z]+)/get_promotion_posts/$', 
        views.get_promotion_posts, 
        name='get_promotion_posts'
    ),
    url(
        r'(?P<fanpage_id>[0-9|a-z]+)/delete_page/$', 
        views.delete_page, 
        name='delete_page'
    ),
    url(
        r'(?P<fanpage_id>[0-9|a-z]+)/posts/$', 
        views.posts, 
        name='delete_page'
    ),
    url(
        r'^addpage',
        views.add_page,
        name='add_page',
    ),
]
