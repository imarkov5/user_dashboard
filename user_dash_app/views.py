from django.shortcuts import render, redirect
from login_reg.models import *
from .models import *
import bcrypt
from django.contrib import messages

def admin(request):
    if request.session['user_level'] == 9:
        context = {
            'all_users': User.objects.all()
        }
        return render(request, 'admin.html', context)
    return redirect('/')

def new_user(request):
    if request.session['user_level'] == 9: 
        if request.method == 'POST':
            errors = User.objects.validate_user(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/users/new_user')
            hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password = hashed_password, user_level = 1)
            return redirect('/users/admin')
        return render(request, 'new_user.html')
    return redirect('/')

def user_info(request):
    return render(request, 'user_info.html')

def dashboard(request):
    if 'user_id' in request.session:
        context = {
            'all_users': User.objects.all()
        }
        return render(request, 'dashboard.html', context)
    return redirect('/')

def edit_user(request, user_id):
    if request.session['user_level'] == 9:
        context = {
            'user': User.objects.get(id=user_id)
        }
        if request.method == 'POST':
            errors = User.objects.validate_edit_user(request.POST, user_id)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/users/{user_id}/edit_user')
            user = User.objects.get(id=user_id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.user_level = request.POST['user_level']
            user.save()
            return redirect(f'/users/{user_id}/edit_user')
        return render(request, 'edit_user.html', context)
    return redirect('/')

def update_password(request):
    errors = User.objects.validate_update_password(request.POST)
    user_id = request.POST['user_id']
    print(user_id)
    print(request.session['user_id'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect(f'/users/{user_id}/edit_user')            
    user = User.objects.get(id=user_id)
    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user.password = hashed_password
    user.save()
    return redirect('/users/admin')
    
def delete_user(request, user_id):
    User.objects.get(id = user_id).delete()
    return redirect('/users/admin')

def profile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        context = {
            'user': User.objects.get(id=request.session['user_id'])
            }
        if request.method == 'POST':
            errors = User.objects.validate_edit_profile(request.POST, user_id)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/users/profile')
            user = User.objects.get(id=request.session['user_id'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return redirect('/users/profile') 
        return render(request, 'profile.html', context)
    return redirect('/')

def profile_password(request):
    errors = User.objects.validate_update_password(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/users/profile')
    user = User.objects.get(id=request.POST['user_id'])
    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    user.password = hashed_password
    user.save()
    return redirect('/users/dashboard')

def edit_description(request):
    errors = User.objects.validate_description(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/users/profile')
    user = User.objects.get(id=request.POST['user_id'])
    user.description = request.POST['description']
    user.save()
    return redirect('/users/profile')