from django.db import models
from mongoengine import *
import mongoengine
from datetime import datetime

class Post(Document):
    fb_id = StringField(unique=True)
    link = StringField()
    message = StringField()
    full_picture = StringField()
    picture = StringField()
    created_time = DateTimeField()

class FanPage(Document):
    link = StringField(unique=True)
    post = ListField(ReferenceField(Post))
    number_of_post = IntField() #so luong bai da lay duoc offset = 100 * k, limit = 100

class User(Document):
    username = StringField()
    password = StringField()
    email = EmailField()
    first_name = StringField()
    last_name = StringField()
    fanpages = ListField(ReferenceField(FanPage, reverse_delete_rule=PULL))
