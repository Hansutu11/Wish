# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from django.db import models

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(alias=post_data['alias'])) > 0:
            # check this user's password
            user = self.filter(alias=post_data['alias'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Alias/Password incorrect.')
        else:
            errors.append('Alias/Password incorrect.')

        if errors:
            return errors
        return user

    # def books_reviewed(self):
    #     return self.model.reviews_left.all().values('book').distict()

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
            errors.append("Name must be at least 3 characters.")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters.")
        # check name fields for letter characters
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Name field must be letter characters.')
        # check emailness of email
        # if not re.match(EMAIL_REGEX, post_data['email']):
        #     errors.append("Invalid Email.")
        # # check uniqueness of email
        # if len(User.objects.filter(email=post_data['email'])) > 0:
        #     errors.append("Email already in use.")
        # # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("Passwords do no match.")

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                alias=post_data['alias'],
                # email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.name

class WishManager(models.Manager):
    def validate_Wish(self, form_data):
        errors = []

        if len(form_data['item']) < 3:
            errors.append('Item cannot be blank. Item must be at least 3 characters!!!')
        return errors

class Wish(models.Model):
    user = models.ForeignKey(User, related_name="wishes")
    item = models.CharField(max_length=255)
    wishers = models.ManyToManyField(User, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
