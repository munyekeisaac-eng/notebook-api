from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password,check_password
from datetime import datetime, timezone, timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
        
    def verify_password(self, password):
        return check_password(password, self.password)    


class Tag(models.Model):
    tagName = models.CharField(max_length=200)
    userId = models.ForeignKey(User, blank=True,null=True, on_delete=models.CASCADE)
    

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tagId = models.ForeignKey(Tag, blank=True,null=True, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, blank=True,null=True, on_delete=models.CASCADE)

class Todo(models.Model):
    title = models.CharField(max_length=200)
    tagId = models.ForeignKey(Tag, blank=True,null=True, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, blank=True,null=True, on_delete=models.CASCADE)

class TodoItem(models.Model):
    content = models.TextField()
    status = models.BooleanField(default=False)
    todoId = models.ForeignKey(Todo, blank=True,null=True, on_delete=models.CASCADE)
    
class OTP(models.Model):
    code = models.IntegerField()
    user_id = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    expires_at = models.DateTimeField(default=datetime.now(timezone.utc)+timedelta(seconds=180))
    created_at = models.DateTimeField(default=datetime.now(timezone.utc))