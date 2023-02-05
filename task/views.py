from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import django.utils.timezone as django_timezone
import pytz
import os
from .serializers import (
    CreateUserSerializer,
    ProfileUserSerializer,
    UserSerializer,
    UpdateUserSerializer,
    PasswordUserSerializer,
    ImagenProfileUserSerializer,
    TaskCreateSerializer,
    TaskUserViewSerializer,
    TaskUpdateSerializer,
    TagsCreateSerializer,
    TagUserViewSerializer)
from .models import UserProfile, Task, Tag


class UserRegisterAPIView(APIView): # Registro de Usuarios

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            UserProfile.objects.create_user(
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get('password'),
                email=serializer.validated_data.get('email')
                )
            return Response({"Success" : "registered user"}, status=status.HTTP_201_CREATED)
        else:    
            return Response({"RegisterError" : "enter the fields correctly"}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView): # Login de usuarios

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login_user = UserProfile.objects.get(username=username)
            login_user.last_login = django_timezone.now().astimezone(pytz.timezone("America/Argentina/Buenos_Aires"))
            login_user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key,
                 'User' : UserSerializer(user).data,
                 'Message' : 'Login Successfully'   
                }, status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response({"Error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView): # Logout de usuarios
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        user.save()
        return Response({"Message": "Logout Successfully"}, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView): # Perfil de usuario
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = ProfileUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class UserProfileUpdateAPIView(APIView): # Actualzicion de perfil de usuario
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            if 'first_name' in serializer.data:
                user.first_name = serializer.validated_data.get('first_name')
            if 'last_name' in serializer.data:
                user.last_name = serializer.validated_data.get('last_name')
            if 'email' in serializer.data:
                user.email = serializer.validated_data.get('email')
            user.save()
            return Response(
                {'Message' : 'Update Profile successfully'},
                 status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"Error" : 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserPasswordUpdateAPIView(APIView): # Actualizar o cambiar contraseña de usuario
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = PasswordUserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            if not user.check_password(password):
                user.set_password(password)
                user.save()
                token = Token.objects.get(user=user)
                token.delete()
                return Response(
                        {'Message' : 'Password Change Successfully'},
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {'Error': f'{password} this password already exists'},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'Error' : 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserImagenProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ImagenProfileUserSerializer(data=request.data)
        if serializer.is_valid():
            old_imagen = user.imagen_profile
            if old_imagen:
                if old_imagen.path and os.path.exists(old_imagen.path):
                    os.remove(old_imagen.path)
            
            user.imagen_profile = serializer.validated_data.get('imagen_profile')
            user.save()
            return Response(
                {'Message' : 'Imagen Profile update successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'Error' : 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserDeleteAPIView(APIView): # Borrar cuenta del usuario
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        user.delete()
        return Response(
            {"Messsage": 'Good bye blue Sky'},
            status=status.HTTP_204_NO_CONTENT
            )

class TaskCreateAPIVIew(APIView): # Creacion de tarea del usuario
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        user = request.user
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            task = Task.objects.create(
                user=user,
                title=title,
                description=serializer.validated_data.get('description'),
                content=serializer.validated_data.get('content'),
                complete=serializer.validated_data.get('complete'),
            )
            tags = serializer.validated_data.get('tags')
            if tags:
                for tag in tags:
                    task_tag, created = Tag.objects.get_or_create(user=request.user, name_tag=tag.get('name_tag'))
                    task.tags.add(task_tag)
            task.creat_at=django_timezone.now().astimezone(pytz.timezone("America/Argentina/Buenos_Aires"))
            task.last_edit=django_timezone.now().astimezone(pytz.timezone("America/Argentina/Buenos_Aires"))
            task.save()
            return Response(
                {'Message': f'Task: |{title} Create successfully'},
                status=status.HTTP_201_CREATED
            )                                                          
        else:
            return Response(
                {'Error': 'the fields are not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

class TaskUserViewAPIView(APIView): # Todas las tareas del usuario
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        task = Task.objects.filter(user=user)
        serializer = TaskUserViewSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class TaskUpdateAPIView(APIView): # Actualizacion de tareas 
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskUpdateSerializer(task, data=request.data, context={'view': self, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteAPIView(APIView): # Borrar tareas
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id):
        user = request.user
        task = Task.objects.get(id=task_id)
        if not task.user != user:
            task.delete()
            return Response(
            {"Messsage": 'Delete Task successfully'},
            status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"Error" : "You do not have permissions to update this task."},
                status=status.HTTP_400_BAD_REQUEST
            )

class TagCreateAPIView(APIView): # Crear etiquetas del usuario
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = TagsCreateSerializer(data=request.data)
        if serializer.is_valid():
            tag = Tag.objects.create(
                user = user,
                color = serializer.validated_data.get('color'),
                name_tag = serializer.validated_data.get('name_tag')
            )
            tag.save()
            return Response(
                {'Message': 'Tag create successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'Error': 'the fields are not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

class TagUserViewAPIView(APIView): # Etiquetas del usuario
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        tag = Tag.objects.filter(user=user)
        serializer = TagUserViewSerializer(tag, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)