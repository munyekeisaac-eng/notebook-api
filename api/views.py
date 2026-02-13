from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action,permission_classes, api_view
from rest_framework_simplejwt.tokens import RefreshToken 
import random
from .models import User, Tag, Note, Todo, TodoItem, OTP
from .serializers import (
    UserSerializer, TagSerializer, NoteSerializer, TodoSerializer, TodoItemSerializer,
    UserCreateSerializer, LoginSerializer,ResetPasswordSerializer
)
from .utils import sendEmail

@api_view(["GET"])
@permission_classes([AllowAny])
def test_headers(request):
    print(request.headers)
    print(request.META.get("HTTP_AUTHORIZATION"))
    return Response({
        "headers": dict(request.headers),
        "authorization_header": request.META.get("HTTP_AUTHORIZATION")
    })
# Create your views here. 
class AuthViewSet(viewsets.ViewSet):
    permission_classes= [AllowAny]
    # register user
    @action(detail=False,methods=['post'],url_name='register', url_path='register')
    def registerUser(self, request):
        data = request.data
        serializer_data = UserCreateSerializer(data=data)
        serializer_data.is_valid()
        user = User.objects.create(**serializer_data.data)
        # user = serializer_data.save()
        user.set_password(data.get('password'))
        user.save()
        
        # after success registration generate access token and refresh token
        access_tokens = RefreshToken.for_user(user=user)
        
        return Response({
            "access_token": str(access_tokens.access_token),
            "refresh_token": str(access_tokens),
            "user": UserSerializer(user).data
        })
        
    # login
    @action(detail=False,methods=['post'],url_name='login', url_path='login')
    def login(self, request):
        data = request.data
        serializer_data = LoginSerializer(data=data)
        serializer_data.is_valid()
        if not User.objects.filter(email=data.get('email')).exists():
            return Response(data={"message": "Invalid credentials"})
        user = User.objects.filter(email=data.get('email')).first()
        
        if not user.verify_password(data.get('password')):
            return Response(data={"message": "Invalid credentials"})
        
        # generate access token
        
        access_tokens = RefreshToken.for_user(user=user)
        print(f"tokens : {access_tokens.access_token}")
        return Response({
            "access_token": str(access_tokens.access_token),
            "refresh_token": str(access_tokens),
            "user": UserSerializer(user).data
        })
        
    # forget password
    
    @action(detail=False,methods=['post'],url_name='forget-password', url_path='forget-password')
    def forgetPassword(self, request):
        email = request.data.get("email",None)
        if not email:
            return Response({"message": "Email is required"},400)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"message": "Invalid Email address"},400)
        
        # create OTP with user id FK
        code = random.randint(100000,999999)
        OTP.objects.create({
            "code": code,
            "user_id" : user.id
        })
        # send otp via email
        sendEmail(user.email, f"Your OTP code is {code}")
        return Response({"message": "OTP was successfully sent to your email"})
    # reset password
    @action(detail=False,methods=['post'],url_name='reset-password', url_path='reset-password')
    def resetPassword(self, request):
        data = request.data
        serializer = ResetPasswordSerializer(data)
        serializer.is_valid()
        
        # confirm email and validate otp
        user = User.objects.filter(email=data.get("email")).first()
        if not user:
            return Response({"message": "Invalid Email address"},400)
        if not OTP.objects.filter(code = data.get("otp")).filter(user_id = user.id).exists():
            return Response({"message": "Invalid Email address"},400)
        # set new password
        user.set_password(data.get("password"))
        user.save()
                
        access_tokens = RefreshToken.for_user(user=user)
        print(f"tokens : {access_tokens.access_token}")
        return Response({
            "access_token": str(access_tokens.access_token),
            "refresh_token": str(access_tokens),
            "user": UserSerializer(user).data
        })
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     user = self.request.user
    #     return super().get_queryset() if 'admin' in user.groups else []


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(userId=user)
    
    # on create set userid to authenticated user id
    def perform_create(self, serializer):
        serializer.save(userId=self.request.user)
    
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(userId=user)
    # on create set userid to authenticated user id
    def perform_create(self, serializer):
        serializer.save(userId=self.request.user)
    
    
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(userId=user)
    
    # on create set userid to authenticated user id
    def perform_create(self, serializer):
        serializer.save(userId=self.request.user)
    
class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter todo items where the parent Todo belongs to the current user
        return super().get_queryset().filter(todoId__userId=user)
    
    # on create set userid to authenticated user id
    def perform_create(self, serializer):
        serializer.save(userId=self.request.user)