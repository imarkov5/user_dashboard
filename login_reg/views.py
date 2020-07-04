from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    if 'user_id' in request.session:
        context={
            'logged_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')
    

def register(request):
    if request.method == "POST":
        errors = User.objects.validate_user(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password = hashed_password, user_level = 1)
        request.session['user_id'] = new_user.id
        request.session['user_level'] = new_user.user_level
        return redirect('/users/dashboard')
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        errors = User.objects.validate_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            request.session['user_level'] = user.user_level
            if user.user_level == 9:
                return redirect('/users/admin')
            else:
                return redirect('/users/dashboard')
    return render(request, 'signin.html')

def logoff(request):
    request.session.flush()
    return redirect('/')


# Create your views here.
