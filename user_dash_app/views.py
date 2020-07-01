from django.shortcuts import render, redirect

def admin(request):
    return render(request, 'admin.html')

def new_user(request):
    return render(request, 'new_user.html')

def user_info(request):
    return render(request, 'user_info.html')
