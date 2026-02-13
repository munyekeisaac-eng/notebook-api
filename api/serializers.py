from rest_framework import serializers
from .models import User, Tag, Note, Todo, TodoItem, OTP

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=500)
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    password = serializers.CharField(max_length=500)
    conf_password = serializers.CharField(max_length=500)
    def validate(self, attrs):
        if attrs["password"] != attrs["conf_password"]:
            return serializers.ValidationError({"conf_password": "Passwords do not match"})
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']
        
class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=500)
    last_name = serializers.CharField(max_length=500)
    username = serializers.CharField(max_length=500)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    todoItems = TodoItemSerializer(many=True)
    class Meta:
        model = Todo
        fields = ['id','title','todoItems', 'userId']   
             
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'