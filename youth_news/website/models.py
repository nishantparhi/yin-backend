from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .util import unique_slug_generator
from ckeditor.fields import RichTextField

# Contact Form 
class Contact(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender" )
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact"

    def __str__(self):
        return self.name + "-" +  self.email

# Blog Post
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=400, null=False)

    slug = models.SlugField(max_length=250, null=True, blank=True)
    # blog_content = models.TextField()
    blog_content = RichTextField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(slug_generator, sender=BlogPost)
