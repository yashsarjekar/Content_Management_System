from django.db import models
import jwt
from .managers import UserManager
from datetime import datetime, timedelta,time
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=254,unique=True,db_index=True)
    password = models.CharField(max_length=500)
    full_name = models.CharField(max_length=50)
    phone = models.IntegerField()
    address = models.CharField(max_length=250,blank=True,null=True,default=" ")
    city = models.CharField(max_length=250,blank=True,null=True,default= " ")
    state = models.CharField(max_length=250,blank=True,null=True,default= " ")
    country =  models.CharField(max_length=250,blank=True,null=True, default=" ")
    pincode = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password','full_name','phone','pincode']
    objects = UserManager()
        
    def __str__(self):
        return self.email

class Author(User,PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password','full_name','phone','pincode']
    objects = UserManager()

    def __str__(self):
        return self.email

class Admin(User,PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password','full_name','phone','pincode']
    objects = UserManager()

    def __str__(self):
        return self.email

class Content(models.Model):
    title = models.CharField(max_length=30,blank=False,null=False)
    email = models.EmailField(max_length=254,null=False,default=1)
    body = models.CharField(max_length=300,blank=False,null=False)
    summary = models.CharField(max_length=60, blank=False, null=False)
    document = models.FileField()
    categories = models.CharField(max_length=50,blank=True,null=True)