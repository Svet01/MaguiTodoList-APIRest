# Generated by Django 4.1.6 on 2023-02-06 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_userprofile_imagen_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='imagen_task',
            field=models.ImageField(blank=True, default='', null=True, upload_to='imagentask/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='imagen_profile',
            field=models.ImageField(blank=True, default='', null=True, upload_to='profile/'),
        ),
    ]
