# models.py

from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


    
class Blog(models.Model):
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends')
    author = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    
class MetaData(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='metadata')
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"
