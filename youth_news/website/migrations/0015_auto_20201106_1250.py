# Generated by Django 3.1.2 on 2020-11-06 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20201106_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='catagories',
            field=models.ManyToManyField(blank=True, null=True, to='website.Catagory'),
        ),
    ]