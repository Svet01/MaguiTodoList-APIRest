from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import django.utils.timezone as django_timezone
import pytz
from pytz import timezone
from datetime import datetime


class Tag(models.Model):
    class Color(models.TextChoices):
        RED = '#FF0000'
        ORANGE = '#FFA500'
        YELLOW = '#FFFF00'
        GREEN = '#00FF00'
        BLUE = '#0000FF'
        PURPLE = '#800080'
        PINK = '#FFC0CB'
        BLACK = '#000000'
        WHITE = '#FFFFFF'
        GRAY = '#808080'
        BROWN = '#A52A2A'
        BEIGE = '#F5F5DC'
        TURQUOISE = '#40E0D0'
        CYAN = '#00FFFF'
        MAGENTA = '#FF00FF'
        LAVENDER = '#E6E6FA'
        MAROON = '#800000'
        OLIVE = '#808000'
        TEAL = '#008080'

    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=False, blank=False, related_name='tags_for_user')
    color = models.CharField(max_length=7, null=True, blank=True, choices=Color.choices, default=Color.GREEN)
    name_tag = models.CharField(max_length=128, null=False, blank=False)

    class Meta:
        ordering = ['name_tag']

    def __str__(self):
        return f'Name Tag: {self.name_tag} Color: {self.color}'



class Task(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=False, blank=False, related_name='task_for_user')
    title = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=80 ,null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags_in_task', default=None)
    creat_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)


    class Meta:
        ordering = ['creat_at']

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Content: {self.content}, Tags: {self.tags}, Create: {self.creat_at.day}/{self.creat_at.month}/{self.creat_at.year} Hour: {self.creat_at.hour}:{self.creat_at.minute}"

    def save(self, *args, **kwargs):
        self.last_edit = django_timezone.now().astimezone(pytz.timezone("America/Argentina/Buenos_Aires"))
        super().save(*args, **kwargs)

class UserManager(BaseUserManager):

    def create_user(self, username, password, email):
        if username:
            if self.filter(username=username).exists():
                return ValidationError('Username is in valid')
        else:
            return ValidationError('Username is required')
        if not password:
            return ValidationError('Password is required')
        if email:
            if self.filter(email=email).exists():
                return ValidationError('Email is in valid')
        else:
            return ValidationError('Email is required')
        user = self.model(
            username=username,
            email=email,
        )
        user.date_joined = django_timezone.now().astimezone(pytz.timezone("America/Argentina/Buenos_Aires"))
        user.set_password(password)
        user.save()
        return user

class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    imagen_profile = models.ImageField(null=True, blank=True, default='', upload_to='profile/')  
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager() # Administrador de la tabla
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):      # Username Legible para humanos
        return f'Usuario: {self.username} ultimo ingreso: {self.date_joined} email: {self.email}'