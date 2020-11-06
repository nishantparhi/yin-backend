# Generated by Django 3.1.2 on 2020-11-06 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20201106_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='catagory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.catagory'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(null=True, to='website.Tag'),
        ),
    ]
