from __future__ import unicode_literals
import bcrypt
from django.db import models
from django.contrib import messages
from django.contrib.sessions.models import Session

from django.conf import settings


# Create your models here.
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def login(self,email,passwd):
		user = self.filter(email=email).first()

		if user and passwd == user.password:
			return (True, user)
		else:

			return (False)




    def register(self,first_name,last_name,email,pwd):
            error = []
            if len(first_name) < 2 or not NAME_REGEX.match(first_name):
                error.append("Invalid First Name")
                print "Failed"

            if len(last_name ) < 2 or not NAME_REGEX.match(last_name):
                error.append("Invalid Last Name")
                print "fail"

            if not EMAIL_REGEX.match(email):
                error.append("Invalid Email")
                print "NO EMAIL"

            if len(error) > 0:
                 return(False,error)
            else:
                user = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pwd)
                user.save()
                #new = user.first_name
                return(True,user)
class WishManager(models.Manager):
    def create_item(self,user_id, wish):
       user = User.objects.get(id=user_id)
       print "Got Here"
       print user
       if len(wish) == 0:
           return (False)
       if len(wish) < 4:
           return (False)

       else:
           wishes =  Wish.objects.create(created_by=user, item=wish)
           wishes.save()
           return (True,wishes)



    def add(self, request, id):
        other_users = User.objects.get(id=request.session['user_id'])
        item = Wish.objects.get(id=id)
        item.other_users.add(other_users)
        return True


    def delete(self, request, id):
        item = Wish.objects.get(id=id)
        item.delete()
        return True


    def remove(self, request, id):
        other_users = User.objects.get(id=request.session['user_id'])
        item = Wish.objects.get(id=id)
        item.other_users.remove(other_users)
        return True




class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    password = models.CharField(max_length=255)
    objects = UserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name+" "+self.email+" "+self.password

class Wish(models.Model):
    item = models.CharField(max_length=100)
    other_users = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, related_name="list")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = WishManager()




# Create your models here.
