# Generated by Django 4.1.6 on 2023-02-14 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_task_imagen_task_alter_userprofile_imagen_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='imagen_task',
            field=models.ImageField(blank=True, default='', null=True, upload_to='imagen-task/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='tags_in_task', to='task.tag'),
        ),
    ]
