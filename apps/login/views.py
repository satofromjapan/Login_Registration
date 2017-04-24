from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt
# Create your views here.
def index(request):
    request.session['first_name'] = ""
    return render(request, 'login/index.html')

def success(request):
    current_user = User.objects.get(id=request.session['id'])
    context = {
    "current_user": current_user,
    }
    return render(request, 'login/success.html', context)

def register(request):
    # user = User.objects.register(request.POST)
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    data = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "password": password,
    "confirm_password": confirm_password
    }
    user = User.objects.register(data)

    if user:
        for i in range(0,len(user)):
            messages.error(request, user[i])
            return redirect('/')
    else:
        request.session['first_name']=request.POST['first_name']
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        create = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed)
        return redirect('/success')


def login(request):
    email = request.POST['email']
    password = request.POST['password']
    data = {"email": email, "password": password}

    user = User.objects.login(data)

    if user:
        for i in range(0,len(user)):
            messages.error(request, user[i])
            return redirect('/')

    else:
        current_user = User.objects.get(email=email)
        print current_user.first_name
        print current_user.id

        request.session['id'] = current_user.id
        return redirect('/success')

def logout(request):
    request.session['first_name'] = ''
    request.session['id'] = ''
    return redirect('/')
