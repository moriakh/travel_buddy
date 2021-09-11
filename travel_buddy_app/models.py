import datetime
from datetime import date
from django.db import models
import re

class UserManager(models.Manager):
    def validate(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        only_letters = re.compile(r'^[a-zA-Z. ]+$')
        errors = {}

        if len(postData['name']) < 3:
            errors['name_len'] = "Name should be at least 3 characters";
        if len(postData['username']) < 3:
            errors['username_len'] = "Username should be at least 3 characters";
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid e-mail"
        if not only_letters.match(postData['name']):
            errors['only_letters'] = "Name should be only letters"
        if len(postData['password']) < 8:
            errors['password_len'] = "Password should be at least 8 characters";
        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "Passwords don't match"
        return errors

class TripsManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if datetime.datetime.strptime(postData['start_date'], "%Y-%m-%d").date() <= datetime.date.today():
            errors['wrong_start_date'] = "Travel dates should be future-dated"
        if datetime.datetime.strptime(postData['end_date'], "%Y-%m-%d").date() <= datetime.datetime.strptime(postData['start_date'], "%Y-%m-%d").date():
            errors['wrong_end_date'] = "Travel Date To should not be before the Travel Date From"
        if len(postData['description_plan']) <= 1:
            errors['empty_plan'] = "You should describe your trip plan"
        return errors

class Users(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 255, unique = True)
    password = models.CharField(max_length = 70)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

class Trips(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    plan = models.CharField(max_length = 255)
    owner_user = models.ForeignKey(Users, related_name = 'own_trips', on_delete = models.CASCADE, null = True, blank = True)
    user = models.ManyToManyField(Users, related_name = 'trips')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripsManager()