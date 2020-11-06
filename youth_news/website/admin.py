from django.contrib import admin
from .models import Contact, BlogPost, Tag, Catagory
# Register your models here.

admin.site.register(Contact)
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Catagory)
