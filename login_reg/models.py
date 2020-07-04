from django.db import models
import bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name'] = "FIrst name must be at least 2 characters and letters only"
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must be at least 2 characters and letters only"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['conf_password']:
            errors['conf_password'] = "Your password and Confirm password must match"
        if len(postData['email']) < 1:
            errors['email'] = "Email field can't be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid"
        elif check:
            errors['email'] = "Email address already registered"
        return errors
    
    def validate_login(self, postData):
        errors = {}
        check_user = User.objects.filter(email=postData['email'])
        if not check_user:
            errors['login_email'] = "Email has not been registered"
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check_user[0].password.encode()):
                errors['login_email'] = "Email and password do not match"
        return errors

    def validate_edit_user(self, postData, user_id):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        user = User.objects.get(id=user_id)
        if len(postData['email']) < 1:
            errors['email'] = "Email field can't be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid"
        elif check and postData['email'] != user.email:
            errors['email'] = "Email address already registered"
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name'] = "FIrst name must be at least 2 characters and letters only"
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must be at least 2 characters and letters only"
        if postData['user_level'] == "0":
            errors['user_level'] = "Select user level"
        return errors

    def validate_edit_profile(self, postData, user_id):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        user = User.objects.get(id=user_id)
        if len(postData['email']) < 1:
            errors['email'] = "Email field can't be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid"
        elif check and postData['email'] != user.email:
            errors['email'] = "Email address already registered"
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name'] = "FIrst name must be at least 2 characters and letters only"
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must be at least 2 characters and letters only"
        return errors

    def validate_update_password(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['conf_password']:
            errors['conf_password'] = "Your password and Confirm password must match"
        return errors

    def validate_description(self, postData):
        errors = {}
        if len(postData['description']) < 10:
            errors['description'] = "Description must be at least 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField(blank=True, null=True)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


