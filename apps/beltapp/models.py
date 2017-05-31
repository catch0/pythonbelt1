from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import datetime
class UserManager(models.Manager):
    def validate(self, form_data):
        print "Inside User.objects.validate method."
        result = {'pass': True}
        errors = []
        #lets see if first name is empty
        if len(form_data['first_name']) == 0:
            errors.append({
                'field': 'first_name', 
                'message': "Yo, can I get yer first name?"
            })
            result['pass'] = False
        #let's see if last name is empty
        if len(form_data['last_name']) == 0:
            errors.append({
                'field': 'last_name',
                 'message': "Yo you got a last name or you one of those celebrities that just goes by their first name?."
            })
            result['pass'] = False
        if len(form_data['email']) == 0:
            errors.append({
                'field': 'email', 
                'message': "Email is required."
            })
            result['pass'] = False
        #lets see if our genius user entered a password
        if len(form_data['password']) == 0:
            errors.append({
                'field': 'password', 
                'message': "Password is required."
            })
            result['pass'] = False
        #gotta confirm that password right?
        if len(form_data['password_confirmation']) == 0:
            errors.append({
                'field': 'password_confirmation',
                'message': "Password confirmation is required."
            })
            result['pass'] = False
        #Check if our genius user entered the same pw twice
        if form_data['password'] != form_data['password_confirmation']:
            errors.append({
                'field': 'password_confirmation',
                'message': "Password confirmation must match password."
            })
            result['pass'] = False
        if errors:
            result['errors'] = errors
        return result
    #makin a usah!!!!!
    def createUser(self, form_data):
        password = form_data['password'].encode()
        #Encrypt the sh*t out of that password
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            password = encryptedpw
        )
        return user
    def findUser(self, data):
        user = User.objects.filter(id=data['user_id']).first()
        return user
    def login(self, form_data):
        result = {'pass': True}
        errors = []
        user = User.objects.filter(email=form_data['email']).first()
        #see if email already exists
        if user:
            password = form_data['password'].encode()
            user_pass = user.password.encode()
            #Check if password is correct
            if bcrypt.hashpw(password, user_pass) == user_pass:
                result['user'] = user
                return result
            errors.append({
            'field': 'password',
            'message': 'awww snap, did you forget your password?.'
            })
        else :
            errors.append({
                'field': 'email',
                'message': 'Could not find email Parter! Howz about we register first? .'
            })   
        result['pass'] = False
        result['errors'] = errors
        return result
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Quote(models.Model):
    speaker=models.CharField(max_length=255)
    content=models.TextField()
    submitted=models.ForeignKey(User, related_name="quote")
    liked_by=models.ManyToManyField(User, related_name="liked_by")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    #objects = QuoteManager()
