from os import path

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from taggit.managers import TaggableManager
from tinymce import models as tinymce_models


LEVEL_CHOICES = [
    ('U', 'Undergraduate'),
    ('PG', 'Postraduate'),
    ('P', 'PhD'),
    ('PT', 'Part-Time'),
]


class Module(models.Model):
    """
        A module contains topics that, in turn, contain many resources (files).
    """
    code = models.CharField(max_length=15, unique=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='modules_created',
                                   on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='modules_enrolled',
                                      blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='U')
    created = models.DateTimeField(auto_now_add=True)
    overview = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    # Experimental
    # def save(self, *args, **kwargs):
    #     if not self.code:
    #         self.code = f'{self.title}[:4]{self.id}'
    #         super().save(*args, **kwargs)


class Topic(models.Model):
    """
        A Module has many Topics.
        A Topic contains many Resources.
    """
    module = models.ForeignKey(Module,
                               related_name='topics',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tag = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = tinymce_models.HTMLField()

    def __str__(self):
        return self.title


# Content
class Resource(models.Model):
    """
        A Topic may contain multiple Resources.
        A Generic Relation is used to associate objects from different models
        representing several types.
        Resource types are files, text, video and images.
    """
    object_id = models.PositiveIntegerField()  # PK
    topic = models.ForeignKey(Topic,
                              related_name='resources',
                              on_delete=models.CASCADE)
    resource_type = models.ForeignKey(ContentType,
                                      on_delete=models.CASCADE,
                                      limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})

    # A field related to both previous fields combined
    item = GenericForeignKey('resource_type', 'object_id')


### File Type Abstract Base Model ###

class ItemBase(models.Model):
    """
        This Model is an Abstract Base Class (ABC) that defines all shared fields for files (text,file,image,video) models.
        For each file type, we create a (child) class.
        *NO database table is created for this model!
    """
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='%(class)s_related',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This is an Abstract Base Class Model
        abstract = True

    def __str__(self):
        return self.title



### File Type Classes ###

class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    # Embedded videos (i.e. YouTube)
    url = models.URLField()
