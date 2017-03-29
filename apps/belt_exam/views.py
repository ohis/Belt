
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):

    return render(request,'belt_exam/index.html')


def logout(request):
	request.session.clear()
	return redirect('/')

def  register(request):
    name = request.POST['first_name']
    lname = request.POST['last_name']
    email = request.POST['email']
    pwd = request.POST['password']
    print pwd
    cpwd = request.POST['pw']
    pwds = pwd.encode()
    cpwds = cpwd.encode()
    if not pwd == cpwd or len(pwd) < 8:
        messages.error(request,"passwords do not match or length too short")
        return redirect('/')
    else:
        hashed1 = bcrypt.hashpw(cpwds, bcrypt.gensalt())
        hashed = bcrypt.hashpw(pwds, bcrypt.gensalt())
        if bcrypt.hashpw(pwds, hashed) == hashed:
           print("It Matches!")


    user = User.objects.register(name,lname,email,pwd)
    if user[0] == False:
        #print  user[1][0]
        print "BOOOSSS"
        messages.error(request, 'One or more of your input is invalid')
        return redirect('/')

    print "here"
    print user
    print 'OK'
    users = User.objects.all()
    print "User id ",user[1].id
    request.session['user_id'] = user[1].id
    print users

    context = {
      'user':User.objects.get(id=request.session['user_id']),
      'message':'registered'
    }


    return render(request,'belt_exam/quotes.html',context)


def log(request):
    pwd = request.POST['password1']
    email = request.POST['email1']
    print pwd
    pwds = pwd.encode()
    if  len(pwd)  < 8:
        messages.error(request,"password invalid  or length too short")
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(pwds, bcrypt.gensalt())
        if bcrypt.hashpw(pwds, hashed) == hashed:
           print("It Matches!")
    user = User.objects.login(email,pwd)
    if user == False:
        messages.error(request, 'Unsuccessful login')
        return redirect('/')
    else:

        print "User id ",user[1].id
        request.session['user_id'] = user[1].id
        #User.objects.get(id=request.session['user_id']),

        context = {
          'user':User.objects.get(id=request.session['user_id']),
          'message': 'logged in'
        }
        return render(request,'belt_exam/quotes.html',context)
