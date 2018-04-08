from django.db import models
from mongoengine import *
import mongoengine
from datetime import datetime

class User(Document):
    # name = StringField()
    # first_name = StringField()
    # last_name = StringField(unique_with='first_name')
    country = StringField()
    age = IntField()
    name = StringField()
    
class AwesomerQuery(QuerySet):
    
    def get_awesome(self):
        return self.filter(awesome=True)

class Page(Document):
    # title = StringField(max_length=200, required=True)
    # country = StringField()
    tags = ListField(StringField())
    author = ReferenceField('User')
    awesome = BooleanField()
    meta = {
        'allow_inheritance': True,
        'queryset_class': AwesomerQuery,
    }

class DatedPage(Page):
    date = DateTimeField()

class ExampleFirst(Document):
    # Default an empty list
    values = ListField(IntField(), default=list)

class ExampleSecond(Document):
    # Default a set of values
    values = ListField(IntField(), default=lambda: [1,2,3])

class ExampleDangerous(Document):
    # This can make an .append call to add values to the default (and all the
    # instead to just an object)
    values = ListField(IntField(), default=[1,2,3])

class Comment(EmbeddedDocument):
    content = StringField()

class SurveyResponse(Document):
    date = DateTimeField()
    user = ReferenceField(User)
    answers = DictField()

class ProfilePage(Document):
    content = StringField()

class Employee(Document):
    name = StringField()
    boss = ReferenceField('self')
    profile_page = ReferenceField(
        'ProfilePage', 
        reverse_delete_rule=mongoengine.NULLIFY
    )                                      

class Link(Document):
    url = StringField()

class Post(Document):
    title = StringField(max_length=120, required=True)
    # author = ReferenceField(User)
    # tags = ListField(StringField(max_length=30))
    published = BooleanField()
    publish_date = DateTimeField()

class Bookmark(Document):
    bookmark_object = GenericReferenceField()

class Recipient(Document):
    name = StringField()
    email = EmailField()

'''
from polls.models import *
user = User(country='uk')
user.save()
page = Page(author=user)
page.save()
'''

class BlogPost(Document):
    title = StringField()
    page_views = IntField()
    tags = ListField(StringField())

    @queryset_manager
    def live_posts(doc_cls, queryset):
        # This mau actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.filter(published=True)


class Essay(Document):
    status = StringField(choices=('Published', 'Draft'), required=True)
    pub_date = DateTimeField()

    def clean(self):
        """Ensures that only published essays have a `pub_date` and
        automatically sets the pub_date if published and not set"""
        if self.status == 'Draft' and self.pub_date is not None:
            msg = 'Draft entries should not have a publication date.'
            raise ValidationError(msg)
        # Set the pub_date for published items if not set.
        if self.status == 'Published' and self.pub_date is None:
            self.pub_date = datetime.now()

class Film(Document):
    title = StringField()
    year = IntField()
    rating = IntField(default=3)


