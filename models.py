from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.first_name + " " + self.last_name



class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('about', 'Hakkımızda'),
        ('hr', 'İnsan Kaynakları'),
        ('training', 'Kurumsal Eğitim'),
        ('software', 'Yazılım Hizmeti')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextUploadingField()
    meta_description = models.CharField(max_length=160, blank=True)
    main_description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='about')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title






class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email