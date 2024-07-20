# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Sum, F
from apps.households.models import *
from apps.schedule.models import *


def index(request):
    try:
        request.session['login_info']
    except Exception as e:
        return redirect('/login/')

    population = sum(Barangay.objects.all().values_list('population', flat=True))
    household = len(Households.objects.all())
    catholic = sum(Households.objects.all().values_list('catholic', flat=True))
    count = Barangay.objects.all().annotate(brgy=F('name')).values('brgy').annotate(total=Sum('population')).values('total')
    name = Barangay.objects.all().order_by('name').values('name').distinct()
    baptized = sum(Households.objects.all().values_list('not_baptized', flat=True))
    lumon = Lumon.objects.values("households_id").distinct().annotate(total=Sum('catholic')).values('total')
    stats = Barangay.objects.values("name").distinct().annotate(total=Sum('catholic')).values('total').order_by('name')
    users = Users.objects.filter(status="Active")
    brgy = len(name)
    hec = len(Barangay.objects.all())
    rec = Records.objects.all()[:3:-1]
    sched = Schedule.objects.all()[:3:-1]
    for obj in rec:
        user = Users.objects.get(id=obj.user)
        obj.user = user
    context = {'segment': 'dashboard', 'population': population, 'catholic': catholic, 'brgy': brgy, 'sched': sched,
               'baptized': baptized, 'count': count, 'stats': stats, 'lumon': lumon, 'users': users, 'rec': rec,
               'name': name, 'hec': hec, 'household': household}
    return render(request, 'home/dashboard.html', context)


def indexAll(request):
    try:
        request.session['login_info']
    except Exception as e:
        return redirect('/login/')

    population = sum(Barangay.objects.all().values_list('population', flat=True))
    catholic = sum(Households.objects.all().values_list('catholic', flat=True))
    count = Barangay.objects.all().annotate(total=Sum('population')).values('total').order_by('name')
    name = Barangay.objects.all().order_by('name').values('name', 'location')
    baptized = sum(Households.objects.all().values_list('not_baptized', flat=True))
    lumon = Lumon.objects.values("households_id").distinct().annotate(total=Sum('catholic')).values('total')
    stats = Barangay.objects.all().annotate(total=Sum('catholic')).values('total').order_by('name')
    users = Users.objects.filter(status="Active")
    brgy = len(name)
    hec = len(Barangay.objects.all())
    rec = Records.objects.all()[:3:-1]
    sched = Schedule.objects.all()[:3:-1]
    for obj in rec:
        user = Users.objects.get(id=obj.user)
        obj.user = user
    context = {'segment': '1', 'population': population, 'catholic': catholic, 'brgy': brgy, 'sched': sched,
               'baptized': baptized, 'count': count, 'stats': stats, 'lumon': lumon, 'users': users, 'rec': rec,
               'name': name, 'hec': hec}
    return render(request, 'home/dashboard.html', context)


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def users(request):
    try:
        request.session['login_info']
    except Exception as e:
        return redirect('/login/')
    query = Users.objects.all().order_by('status', '-id')
    users = Users.objects.all().values('role').distinct()
    context = {'segment': 'users-access', 'query': query, 'users': users}
    html_template = loader.get_template('users/users.html')
    return HttpResponse(html_template.render(context, request))


def admin(request):
    try:
        request.session['login_info']
    except Exception as e:
        return redirect('/login/')
    query = Admin.objects.all()
    users = Admin.objects.all().values('userrole').distinct()
    context = {'segment': 'users-access', 'query': query, 'users': users}
    html_template = loader.get_template('users/admin.html')
    return HttpResponse(html_template.render(context, request))


def user_view(request, nid):
    if request.method == 'GET':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')
        query = Users.objects.get(id=nid)
        context = {'segment': 'users-access', 'query': query}
        html_template = loader.get_template('users/user_view.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        birthdate = request.POST.get('birthdate')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = Users.objects.filter(id=nid).update(lastname=lastname, firstname=firstname, middlename=middlename, gender=gender,
                                            contact=contact, address=address, birthdate=birthdate, username=username,
                                            password=password, role=role)
        if user:
            return redirect('/users/')


def admin_view(request, nid):
    if request.method == 'GET':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')

        query = Admin.objects.get(id=nid)
        context = {'segment': 'users-access', 'query': query}
        return render(request, 'users/admin_view.html', context)
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        userrole = request.POST.get('userrole')
        status = request.POST.get('status')

        Admin.objects.filter(id=nid).update(name=name, username=username, password=password, userrole=userrole,
                                            status=status)
        return redirect('/admin/')


def deactivate_user(request, nid):
    status = 'Inactive'
    Users.objects.filter(id=nid).update(status=status)
    return redirect('/users/')


def activate_user(request, nid):
    status = 'Active'
    Users.objects.filter(id=nid).update(status=status)
    return redirect('/users/')

