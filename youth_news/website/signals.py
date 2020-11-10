from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Author

def author_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='general_content_writer')
        instance.groups.add(group)

        # add author profile
        Author.objects.create(user=instance)
        # print("Author Created...")

post_save.connect(author_profile, sender=User)