# Generated by Django 4.1.3 on 2023-01-31 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, choices=[('#FF0000', 'Red'), ('#FFA500', 'Orange'), ('#FFFF00', 'Yellow'), ('#00FF00', 'Green'), ('#0000FF', 'Blue'), ('#800080', 'Purple'), ('#FFC0CB', 'Pink'), ('#000000', 'Black'), ('#FFFFFF', 'White'), ('#808080', 'Gray'), ('#A52A2A', 'Brown'), ('#F5F5DC', 'Beige'), ('#40E0D0', 'Turquoise'), ('#00FFFF', 'Cyan'), ('#FF00FF', 'Magenta'), ('#E6E6FA', 'Lavender'), ('#800000', 'Maroon'), ('#808000', 'Olive'), ('#008080', 'Teal')], default='#FF0000', max_length=7, null=True)),
                ('name_tag', models.CharField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_for_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name_tag'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(blank=True, max_length=80, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('creat_at', models.DateTimeField(auto_now_add=True)),
                ('last_edit', models.DateTimeField(auto_now=True)),
                ('complete', models.BooleanField(default=False)),
                ('tags', models.ManyToManyField(related_name='tags_in_task', to='task.tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_for_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['creat_at'],
            },
        ),
    ]
