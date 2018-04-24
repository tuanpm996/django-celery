# from celery import shared_task, current_task, Celery
from celery import shared_task
import facebook
from django.conf import settings
from celery.contrib import rdb
from .models import *
import requests
from datetime import datetime, timedelta


@shared_task
def get_posts(link, fanpage_id):
    fanpage = FanPage.objects(id=fanpage_id)
    offset = 0
    graph = facebook.GraphAPI(access_token=settings.ACCESS_TOKEN, version = 2.12)
    posts = graph.request(link + '/posts?' + '&limit=100&offset=' + str(offset) + '&fields=id,link,message,full_picture,picture,created_time')
    while(len(posts['data']) > 0):
        get_posts_by_data(posts, fanpage[0])
        offset = offset + 100
        print offset
        posts = requests.get(posts['paging']['next']).json()
        print len(posts['data'])

@shared_task
def crontab_get_posts():
    since = (datetime.utcnow() - timedelta(days=1)).strftime("%s")
    until = datetime.utcnow().strftime("%s")
    graph = facebook.GraphAPI(access_token=settings.ACCESS_TOKEN, version = 2.12)
    for fanpage in FanPage.objects():
        link = fanpage.link
        posts = graph.request(
            link 
            + '/posts?' 
            + '&limit=100'
            + '&fields=id,link,message,full_picture,picture,created_time&since=' 
            + since
            + '&until=' + until
        )
        get_posts_by_data(posts, fanpage)

def get_posts_by_data(posts, fanpage):
    for post in posts['data']:
        new_post = None
        for word in settings.LIST_WORDS:
            if post.get('message') and word in post.get('message'):
                try:
                    new_post = Post(
                        fb_id = post.get('id'),
                        link = post.get('link'),
                        message = post.get('message'),
                        full_picture = post.get('picture'),
                    )
                except Exception as e:
                    print e
                break
        try:
            if new_post:
                new_post.save()
                fanpage.update(add_to_set__post=new_post)
        except Exception as e:
            if Post.objects(fb_id=post.get('id')):
                new_post = Post.objects(fb_id=post.get('id'))[0]    
                if new_post:
                    try:
                        fanpage.update(add_to_set__post=new_post)
                    except Exception as e:
                        print e
            print e
        
        
