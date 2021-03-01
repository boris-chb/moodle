from moodle.settings import AUTH_USER_MODEL
from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Module(models.Model):
    """
        A module contains topics that, in turn, contain many resources (files).
    """
    instructor = models.ForeignKey(AUTH_USER_MODEL, related_name='courses_created',
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title


class Topic(models.Model):
    """
        A module has many topics.
        A topic contains many resources.
    """
    module = models.ForeignKey(Module,
                               related_name='topics',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title


#     Content
class Resource(models.Model):
    """
        A Topic may contain multiple Resources.
        A Generic Relation is used to associate objects from different models
        representing several file types.
    """
    topic = models.ForeignKey(Topic, related_name='resources',
                              on_delete=models.CASCADE)
    resource_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':
                                         ('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField() # PK
    # A field to the related object combinit
    item = GenericForeignKey('resource_type', 'object_id')


# File Type Abstract Base Model
class ItemBase(models.Model):
    """
        For each file type, we create a (child) class.
        The fields used by each of file (child) classes are defined in this (parent) ItemBase class.
        !NO database table is created for this model.
    """
    creator = models.ForeignKey(AUTH_USER_MODEL,
                                related_name='%(class)s_related',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Abstract Base Model
        abstract = True
    
    def __str__(self):
        return self.title

# File Type Classes
class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

