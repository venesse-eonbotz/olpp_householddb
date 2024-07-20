# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from apps.schedule.models import *
from .forms import SignUpForm
from datetime import date
from .models import *


def login_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        current_user = Users.objects.filter(username=username)
        if len(current_user) == 1:
            try:
                user = Users.objects.get(username=username, password=password)
            except Exception as e:
                print(e)
                msg = 'Invalid credentials'
                return render(request, "accounts/login.html", {"msg": msg})

            if user is not None:
                request.session['login_info'] = {'id': user.id, 'username': user.username,  'password': user.password,
                                                 'lastname': user.lastname, 'firstname': user.firstname,
                                                 'role': user.role, 'gender': user.gender}
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            try:
                Admin.objects.get(username=username, password=password)
            except Exception as e:
                print(e)
                msg = 'Invalid credentials'
                return render(request, "accounts/login.html", {"msg": msg})

            user = Admin.objects.get(username=username, password=password)
            if user is not None:
                request.session['login_info'] = {'id': user.id, 'username': user.username,  'password': user.password,
                                                 'name': user.name, 'userrole': user.userrole}
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        return render(request, "accounts/login.html", {"msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def add_users(request):
    if request.method == 'GET':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')

        context = {'segment': 'add-users'}
        return render(request, 'accounts/add_users.html', context)
    if request.method == 'POST':
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        birthdate = request.POST.get('birthdate')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        date_started = date.today()
        status = "Active"
        Users.objects.create(lastname=lastname, firstname=firstname, middlename=middlename, birthdate=birthdate,
                             username=username, password=password, contact=contact, address=address, role=role,
                             date_started=date_started, status=status, gender=gender)
        return redirect('/users/')


def add_admin(request):
    if request.method == 'GET':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')

        context = {'segment': 'add-admin'}
        return render(request, 'accounts/add_admin.html', context)
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        userrole = request.POST.get('userrole')
        status = request.POST.get('status')
        Admin.objects.create(name=name, username=username, password=password, userrole=userrole, status=status)
        return redirect('/admin/')


def logout(request):
    request.session.clear()
    return redirect('/login/')
