from apps.schedule.models import Schedule, Records
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.households.models import *
from apps.authentication.models import *
import datetime


# Create your views here.
def schedules(request):
    if 'q' in request.GET:
        q = request.GET.get('q', '')
        # pvt_list = pvt_data.objects.filter(full_name__icontains=q)
        sched = Schedule.objects.filter(task__icontains=q).order_by('-id')
        date_today = datetime.datetime.now().date()
        p = Paginator(sched, 2)  # Show 5 tasks per page.
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(1)

        context = {'segment': 'schedules', 'sched': sched, 'date_today': date_today, 'items': page}
        return render(request, 'schedule/schedules.html', context)
    if request.method == 'GET':
        sched = Schedule.objects.all().order_by('-id')
        date_today = datetime.datetime.now().date()
        p = Paginator(sched, 2)  # Show 5 tasks per page.
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(1)
        context = {'segment': 'schedules', 'sched': sched, 'date_today': date_today, 'items': page}
        return render(request, 'schedule/schedules.html', context)
    return render(request, 'schedule/schedules.html')


def taskSearch(request):
    if 'q' in request.GET:
        q = request.GET.get('q', '')
        # pvt_list = pvt_data.objects.filter(full_name__icontains=q)
        sched = Schedule.objects.filter(task__icontains=q).order_by('-id')
        date_today = datetime.datetime.now().date()
        p = Paginator(sched, 2)  # Show 5 tasks per page.
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(1)

        context = {'segment': 'schedules', 'sched': sched, 'date_today': date_today, 'items': page}
        return render(request, 'schedule/schedules.html', context)
    else:
        return render(request, 'schedule/schedules.html')


def my_schedules(request):
    user = request.session['login_info'].get('id')
    # sched = Schedule.objects.filter(user=user).order_by('-id')
    # date_today = datetime.datetime.now().date()
    # context = {'segment': 'schedules', 'items': sched, 'date_today': date_today}
    # return render(request, 'schedule/schedules.html', context)
    if 'q' in request.GET:
        q = request.GET.get('q', '')
        # pvt_list = pvt_data.objects.filter(full_name__icontains=q)
        sched = Schedule.objects.filter(task__icontains=user, user=user).order_by('-id')
        date_today = datetime.datetime.now().date()
        p = Paginator(sched, 2)  # Show 5 tasks per page.
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(1)

        context = {'segment': 'schedules', 'sched': sched, 'date_today': date_today, 'items': page}
        return render(request, 'schedule/schedules.html', context)
    else:
        if request.method == 'GET':
            sched = Schedule.objects.filter(user=user).order_by('-id')
            date_today = datetime.datetime.now().date()
            p = Paginator(sched, 2)  # Show 5 tasks per page.
            page_num = request.GET.get('page', 1)

            try:
                page = p.page(page_num)
            except PageNotAnInteger:
                page = p.page(1)
            except EmptyPage:
                page = p.page(1)
            context = {'segment': 'schedules', 'sched': sched, 'date_today': date_today, 'items': page}
            return render(request, 'schedule/schedules.html', context)


def add_schedule(request):
    if request.method == 'GET':
        brgy = Barangay.objects.all()
        users = Users.objects.filter(status="Active")
        context = {'segment': 'schedules', 'users': users, 'brgy': brgy}
        return render(request, 'schedule/schedule_add.html', context)
    if request.method == 'POST':
        users = request.POST.getlist('user')
        date_time = request.POST.get('datetime')
        task = request.POST.get('task')
        description = request.POST.get('description')
        date_today = datetime.datetime.now()
        for user in users:
            Schedule.objects.create(
                user_id=user,
                datetime=date_time,
                dateposted=date_today,
                task=task,
                description=description
            )
        # Schedule.objects.create(user_id=user, datetime=date_time, dateposted=date_today, task=task, description=description)
        return redirect('/schedules/')


def edit_schedule(request, nid):
    if request.method == 'GET':
        brgy = Barangay.objects.all()
        query = Schedule.objects.get(id=nid)
        users = Users.objects.filter(status="Active")
        context = {'segment': 'schedules', 'users': users, 'brgy': brgy, 'query': query}
        return render(request, 'schedule/schedule_edit.html', context)
    if request.method == 'POST':
        user = request.POST.get('user')
        datetime = request.POST.get('datetime')
        task = request.POST.get('task')
        description = request.POST.get('description')
        Schedule.objects.filter(id=nid).update(user_id=user, datetime=datetime, task=task, description=description)
        return redirect('/schedules/')


def records(request):
    try:
        request.session['login_info']
    except Exception as e:
        return redirect('/login/')

    rec = Records.objects.all().order_by('-id')
    for obj in rec:
        user = Users.objects.get(id=obj.user)
        obj.user = user
    context = {'segment': 'records', 'rec': rec}
    return render(request, 'schedule/records.html', context)


def add_record(request):
    if request.method == 'GET':
        brgy = Barangay.objects.all()
        users = Users.objects.filter(status="Active")
        context = {'segment': 'schedule-add', 'users': users, 'brgy': brgy}
        return render(request, 'schedule/schedule_add.html', context)
    if request.method == 'POST':
        user = request.POST.get('user')
        datetime = request.POST.get('datetime')
        task = request.POST.get('task')
        description = request.POST.get('description')
        Schedule.objects.create(user_id=user, datetime=datetime, task=task, description=description)
        return redirect('/schedules/')


def my_record(request):
    try:
        request.session['login_info']
    except Exception as e:
        return redirect('/login/')

    user = request.session['login_info'].get('id')
    rec = Records.objects.filter(user=user).order_by('-id')
    context = {'segment': 'records', 'rec': rec}
    return render(request, 'schedule/records.html', context)
