from rest_framework import serializers
from .models import Tag, Task, UserProfile


class CreateUserSerializer(serializers.ModelSerializer): #Registro de datos

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
        }

class UserSerializer(serializers.ModelSerializer): #Para ver datos al hacer login
    class Meta:
        model = UserProfile
        fields = ['username', 'last_login']

class ProfileUserSerializer(serializers.ModelSerializer): #Ver perfil del usuario
    date_joined = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    last_login = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    class Meta:
        model = UserProfile
        fields = ['username','email', 'first_name', 'last_name', 'date_joined', 'last_login', 'imagen_profile']

class UpdateUserSerializer(serializers.ModelSerializer): #Actualizar perfil del usuario
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name']

class PasswordUserSerializer(serializers.ModelSerializer): #Actualizer Password del usuario
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

class ImagenProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['imagen_profile']
        extra_kwargs = {
            'imagen_profile' : {'required' : True}
        }

class Colors(object):
    def __init__(self, choices):
        self.choices = choices

COLORS_CHOICES =( 
    ("RED", '#FF0000'),
    ("ORANGE" , '#FFA500'),
    ("YELLOW" , '#FFFF00'),
    ("GREEN" , '#00FF00'),
    ("BLUE" , '#0000FF'),
    ("PURPLE" , '#800080'),
    ("PINK" , '#FFC0CB'),
    ("BLACK" , '#000000'),
    ("WHITE" , '#FFFFFF'),
    ("GRAY" , '#808080'),
    ("BROWN" , '#A52A2A'),
    ("BEIGE" , '#F5F5DC'),
    ("TURQUOISE" , '#40E0D0'),
    ("CYAN" , '#00FFFF'),
    ("MAGENTA" , '#FF00FF'),
    ("LAVENDER" , '#E6E6FA'),
    ("MAROON" , '#800000'),
    ("OLIVE" , '#808000'),
    ("TEAL" , '#008080'),
)

class TagsCreateSerializer(serializers.ModelSerializer): 
    color = serializers.ChoiceField(choices = COLORS_CHOICES)

    class Meta:
        model = Tag
        fields = ['color', 'name_tag']
        extra_kwargs = {
            'color' : {'required' : False},
            'name_tag' : {'required' : True}
        }

class TagUserViewSerializer(serializers.ModelSerializer):    
    user = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['user', 'name_tag', 'color']

    def get_user(self, obj):
        return obj.user.username

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name_tag', 'color']

class TaskCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True)
    creat_at = serializers.ReadOnlyField()
    last_edit = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = ['user', 'tags', 'title', 'description', 'content', 'imagen_task' ,'creat_at', 'last_edit', 'complete']
        extra_kwargs = {
            'tags' : {'required' : False, 'default': None},
            'title' : {'required': True},
            'description': {'required': False, 'default': None},
            'content' : {'required': False, 'default': None},
            'complete' : {'required': False, 'default': False},
            'imagen_task' : {'required' : False, 'default': None}
        }

class TaskUserViewSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user = serializers.SerializerMethodField()
    creat_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    last_edit = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    class Meta:
        model = Task
        fields = ['id', 'user', 'tags', 'title', 'description', 'content', 'imagen_task', 'complete', 'last_edit', 'creat_at']

    def get_user(self, obj):
        return obj.user.username

class TaskUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Task
        fields = ['imagen_task', 'tags' ,'title', 'description', 'content', 'complete']
        extra_kwargs = {
            "title" : {'required' : False},
            "description" : {'required' : False},
            "content" : {'required' : False},
            "complete" : {'required' : False},
            "imagen_task" : {"required" : False}
        }

    def validate(self, data):
        task_id = self.context['view'].kwargs['task_id']
        task = Task.objects.get(id=task_id)
        if task.user != self.context['request'].user:
            raise serializers.ValidationError("You do not have permissions to update this task.")
        return data
    
