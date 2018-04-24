#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from fanpages.models import *
import facebook
import requests
import datetime
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import tasks



def posts(request, fanpage_id):
    if request.GET.get('page'):
        page = int(request.GET['page'])
    else:
        page = 1

    posts = FanPage.objects(id=fanpage_id)[0].post
    paginator = Paginator(posts, 10)

    return render(request, 'fanpages/posts.html', {
        'posts':  paginator.page(page),
    })


def index(request):
    return render(request, 'fanpages/index.html', {'fanpages' : User.objects()[0].fanpages })
    

def get_promotion_posts(request, fanpage_id):

    fanpage = FanPage.objects(id=fanpage_id)
    
    link = fanpage[0].link
    tasks.get_posts.delay(link, fanpage_id)

    return render(request, 'fanpages/success.html')

def add_page(request):
    page = FanPage(request.GET['page_link'])
    try:
        page.save()
    except Exception as e:
        print e
        return JsonResponse(
            {
                'status': 'fail',
                'noti': "Something error",
            }
        )

    user = User.objects()[0]
    user.update(add_to_set__fanpages=page)
    user.save()
    return JsonResponse(
            {
                'status': 'success',
                'noti': "Add page succesfully!",
                'fanpage_id': str(page.id),
                'fanpage_link': page.link,
            }
        )

def delete_page(request, fanpage_id):
    try:
        user = User.objects(fanpages__ = fanpage_id)[0]
        user.update(pull__fanpages=fanpage_id)
        fanpage = FanPage.objects(id=fanpage_id)[0]
        for post in fanpage.post:
            fanpage.update(pull__post=post.id)
            Post.objects(id=post.id).delete()
        FanPage.objects(id=fanpage_id).delete()
    except Exception as e:
        print e
        return redirect(index) 
    return redirect(index)   
