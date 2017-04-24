from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def login(self, info):
        errors= []
        # print info['email']
        users = User.objects.get(email=info['email'])
        # print users
        if users==None:
            errors.append("Invalid Email")
        else:
            users1 = User.objects.get(email=info['email'], password=bcrypt.hashpw(info['password'].encode(), users.password.encode()))
            # print users1
            if not users1:
                errors.append("Login Invalid")

        return errors

    def register(self, info):
        errors=[]

        #Validate First Name
        if len(info['first_name']) < 2 or not info['first_name'].isalpha():
            errors.append('First name is not valid')
        #Validate Last Name
        if len(info['last_name']) < 2 or not info['last_name'].isalpha():
            errors.append('Last name is not valid')
        #Validate Email
        if not EMAIL_REGEX.match(info['email']):
            errors.append('Email is not valid')
        #Validate password
        if len(info['password']) < 8:
            errors.append('Password must be more than 8 characters')
        #Validate password against confirm_password
        if info['password'] != info['confirm_password']:
            errors.append('Password must match confirm password')

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
