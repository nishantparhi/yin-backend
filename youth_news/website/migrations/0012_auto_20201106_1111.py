# Generated by Django 3.1.2 on 2020-11-06 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20201106_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='coverPic',
            field=models.ImageField(default='/static/default_cover.png', upload_to='cover_photos/'),
        ),
    ]
