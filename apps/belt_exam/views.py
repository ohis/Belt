
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):

    return render(request,'belt_exam/index.html')
def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    user_wishlist = Wish.objects.filter(created_by=user)
    users = User.objects.all()
    other_wishlist = Wish.objects.all().exclude(created_by=user).exclude(other_users=user)
    context = {
        'user' : user,
        'user_wishlist' : user_wishlist,
        'co_wishlist' : Wish.objects.filter(other_users=user),
        'other_wishlist' : other_wishlist,
        'created_at': Wish.created_at,
    }
    return render(request, 'belt_exam/dashboard.html', context)

def create_item(request):
    user_id = request.POST['id']
    wish_item = request.POST['wish_item']
    wish = Wish.objects.create_item(user_id, wish_item)
    if wish == False:
        messages.error(request,"Invalid input")
        return redirect('/dashboard')
    else:
        messages.success(request,"Successfully created an item")
        return redirect('/dashboard')


def wish(request, id):
        item = Wish.objects.get(id=id)
        print item.created_by.first_name
        context = {
        'created_by' : Wish.objects.get(id=id).created_by,
        'other_users' : Wish.objects.get(id=id).other_users.all(),
        'item' : item,
        }
        return render(request, 'belt_exam/wish_item.html', context)


def add_new(request):
    return render(request, 'belt_exam/create.html')

def add(request, id):
        print "SUUUUUPPP"
        print "Added"
        wish_list = Wish.objects.add(request, id)
        if wish_list == True :
            messages.success(request, 'You have successfully added this  to your wishlist.')

        else:
            messages.error(request, 'Unsuccessful.')
        return redirect('/dashboard')


def delete(request, id):
        delete = Wish.objects.delete(request, id)
        if delete == True:
            messages.success(request, 'You have deieted this from your wishlist.')

        else:
            messages.error(request, 'Unsuccessful')
        return redirect('/dashboard')


def remove(request, id):

        rem = Wish.objects.remove(request, id)
        if rem == True:
            messages.success(request, 'You have removed this item.')

        else:
            messages.error(request, 'Unsuccessful')
        return redirect('/dashboard')






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


    return render(request,'belt_exam/dashboard.html',context)


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
        return render(request,'belt_exam/dashboard.html',context)
