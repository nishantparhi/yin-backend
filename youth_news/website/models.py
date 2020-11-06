from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .util import unique_slug_generator
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField

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

# Tag model
class Tag(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text

# Tag model
class Catagory(models.Model):
    text = models.CharField(max_length=200)
    tranding = models.BooleanField(default=False)
    def __str__(self):
        return self.text

# Blog Post
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=400, null=False)

    slug = models.SlugField(max_length=250, null=True, blank=True)
    # blog_content = models.TextField()
    # blog_content = RichTextField(blank=True, null=True)
    blog_content = RichTextUploadingField(blank=True, null=True)
    coverPic = models.ImageField(upload_to= 'cover_photos/', default="/cover_photos/default_cover.png")

    pub_date = models.DateTimeField(auto_now_add=True)
    
    BLOG_STATUS_CHOICES = [
    ('ACTIVE', 'ACTIVE'),
    ('PENDING', 'PENDING'),
    ]

    status = models.CharField(max_length=30, choices=BLOG_STATUS_CHOICES, default="PENDING")
    catagory = models.ManyToManyField(Catagory, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    isTranding = models.BooleanField(default=False)

    def __str__(self):
        return self.blog_title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(slug_generator, sender=BlogPost)