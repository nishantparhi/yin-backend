# Generated by Django 3.1.2 on 2020-11-06 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_auto_20201106_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='catagory',
            new_name='catagories',
        ),
    ]
