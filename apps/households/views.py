from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F, Sum
from django.contrib import messages
from django.template import loader
from apps.schedule.models import *
from docxtpl import DocxTemplate
from datetime import datetime
from .models import *
import csv


# Create your views here.
def barangay(request):
    brgy_list = Barangay.objects.all().values('name').distinct()
    brgy = Barangay.objects.all().values('name', 'location', 'population', 'brgy_captain', 'lumon', 'catholic',
                                         'not_baptized', 'not_confirmed', 'not_married', 'professionals',
                                         'stop_highschool', 'stop_college', 'id').order_by('name')
    total = sum(Barangay.objects.all().values_list('population', flat=True))
    lumons = Lumon.objects.values("households_id").distinct().annotate(total=Sum('catholic')).values('total')
    count_brgy = len(brgy_list)
    barangay = []
    for b in brgy:
        id = b['id']
        population = b['population']
        name = b['name']
        location = b['location']
        brgy_captain = b['brgy_captain']
        lumon = b['lumon']
        catholic = b['catholic']
        not_baptized = b['not_baptized']
        not_confirmed = b['not_confirmed']
        not_married = b['not_married']
        professionals = b['professionals']
        stop_highschool = b['stop_highschool']
        stop_college = b['stop_college']
        if population != 0:
            percentage = round(((population / total) * 100), 1)
        else:
            percentage = 0
        barangay.append({
            'name': name, 'brgy_captain': brgy_captain, 'location': location, 'population': population,
            'percentage': percentage, 'lumon': lumon, 'catholic': catholic, 'not_baptized': not_baptized,
            'not_confirmed': not_confirmed, 'not_married': not_married, 'professionals': professionals,
            'stop_highschool': stop_highschool, 'stop_college': stop_college, 'id': id
        })

    context = {'segment': 'barangay', 'brgy': brgy, 'total': total, 'barangay': barangay, 'count_brgy': count_brgy,
               'lumons': lumons, 'brgy_list': brgy_list}
    return render(request, 'master/barangay.html', context)


def barangayByName(request, name):
    bname = name
    hec_list = Barangay.objects.filter(name=name)
    brgy = Barangay.objects.filter(name=name).values('name', 'location', 'population', 'brgy_captain', 'lumon', 'catholic',
                                                     'not_baptized', 'not_confirmed', 'not_married', 'professionals',
                                                     'stop_highschool', 'stop_college', 'id').order_by('name')
    total = sum(Barangay.objects.all().values_list('population', flat=True))
    lumons = Lumon.objects.values("households_id").distinct().annotate(total=Sum('catholic')).values('total')
    count_hec = len(hec_list)
    barangay = []
    for b in brgy:
        id = b['id']
        population = b['population']
        name = b['name']
        location = b['location']
        brgy_captain = b['brgy_captain']
        lumon = b['lumon']
        catholic = b['catholic']
        not_baptized = b['not_baptized']
        not_confirmed = b['not_confirmed']
        not_married = b['not_married']
        professionals = b['professionals']
        stop_highschool = b['stop_highschool']
        stop_college = b['stop_college']
        if population != 0:
            percentage = round(((population / total) * 100), 1)
        else:
            percentage = 0
        barangay.append({
            'name': name, 'brgy_captain': brgy_captain, 'location': location, 'population': population,
            'percentage': percentage, 'lumon': lumon, 'catholic': catholic, 'not_baptized': not_baptized,
            'not_confirmed': not_confirmed, 'not_married': not_married, 'professionals': professionals,
            'stop_highschool': stop_highschool, 'stop_college': stop_college, 'id': id
        })
    context = {'segment': 'barangay', 'brgy': brgy, 'total': total, 'barangay': barangay, 'count_hec': count_hec,
               'lumons': lumons, 'hec_list': hec_list, 'bname': bname}
    return render(request, 'master/barangay-view-by-name.html', context)


def add_barangay(request):
    if request.method == 'GET':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')
        context = {'segment': 'households'}
        html_template = loader.get_template('master/barangay_add.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        brgy_captain = request.POST.get('brgy_captain')
        Barangay.objects.create(name=name, location=location, brgy_captain=brgy_captain)
        msg = "Your work has been saved"
        messages.success(request, f'{msg}')
        return redirect('/barangay/')


def edit_barangay(request, nid):
    if request.method == 'GET':
        query = Barangay.objects.get(id=nid)
        household = len(Households.objects.filter(barangay=nid))
        if query.population != 0:
            population = format(((query.population / sum(Barangay.objects.all().values_list('population', flat=True))) * 100), ".0f")
        else:
            population = 0
        if query.lumon != 0:
            lumon = format(((query.lumon / query.population) * 100), ".0f")
        else:
            lumon = 0
        if query.catholic != 0:
            catholic = format(((query.catholic / query.population) * 100), ".0f")
        else:
            catholic = 0
        if query.not_baptized != 0:
            not_baptized = format(((query.not_baptized / query.population) * 100), ".0f")
        else:
            not_baptized = 0
        if query.not_confirmed != 0:
            not_confirmed = format(((query.not_confirmed / query.population) * 100), ".0f")
        else:
            not_confirmed = 0
        if query.not_married != 0:
            not_married = format(((query.not_confirmed / query.population) * 100), ".0f")
        else:
            not_married = 0
        if query.professionals != 0:
            professionals = format(((query.professionals / query.population) * 100), ".0f")
        else:
            professionals = 0
        if query.stop_highschool != 0:
            stop_highschool = format(((query.stop_highschool / query.population) * 100), ".0f")
        else:
            stop_highschool = 0
        if query.stop_college != 0:
            stop_college = format(((query.stop_college / query.population) * 100), ".0f")
        else:
            stop_college = 0
        context = {'segment': 'households', 'query': query, 'household': household}
        return render(request, 'master/barangay_edit.html', context | locals())
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        brgy_captain = request.POST.get('brgy_captain')
        Barangay.objects.filter(id=nid).update(name=name, location=location, brgy_captain=brgy_captain)
        return redirect('/barangay/')


def csv_barangay(request):
    brgy = Barangay.objects.all().order_by('name', 'location')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Report1.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'HEC' 'Population', 'Lumon', 'Catholic Residence', 'NOT Baptized', 'NOT Confirmed',
                     'NOT Married', 'Professionals', 'STOPPED High School', 'STOPPED College'])  # header
    for item in brgy:
        writer.writerow([item.name, item.location, item.population, item.lumon, item.catholic, item.not_baptized,
                         item.not_confirmed, item.not_married, item.professionals, item.stop_highschool,
                         item.stop_college])  # rows

    return response


def csv_barangayByName(request, name):
    brgy = Barangay.objects.filter(name=name).order_by('location')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Report-{name}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'HEC' 'Population', 'Lumon', 'Catholic Residence', 'NOT Baptized', 'NOT Confirmed',
                     'NOT Married', 'Professionals', 'STOPPED High School', 'STOPPED College'])  # header
    for item in brgy:
        writer.writerow([item.name, item.location, item.population, item.lumon, item.catholic, item.not_baptized,
                         item.not_confirmed, item.not_married, item.professionals, item.stop_highschool,
                         item.stop_college])  # rows
    return response


def word_barangay(request, nid):
    brgy = Barangay.objects.get(id=nid)
    doc = DocxTemplate("apps/households/word_templates/Barangay.docx")

    data = {
        'name': brgy.name,
        'population': brgy.population,
        'lumon': brgy.lumon,
        'catholic': brgy.catholic,
        'not_married': brgy.not_married,
        'not_baptized': brgy.not_baptized,
        'not_confirmed': brgy.not_confirmed,
        'professionals': brgy.professionals,
        'stop_highschool': brgy.stop_highschool,
        'stop_college': brgy.stop_college,
    }

    doc.render(data)
    doc.save(f'C:\\Users\\EonBotz 5\\Downloads\\{brgy.name}.docx')

    return redirect('/barangay/')


def households(request):
    brgy = Barangay.objects.all().values('name').distinct()
    if request.method == 'GET':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')
        household = Households.objects.all().order_by('-id')
        context = {'segment': 'households', 'household': household, 'brgy': brgy}
        html_template = loader.get_template('master/households.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        try:
            request.session['login_info']
        except Exception as e:
            return redirect('/login/')
        barangay = request.POST.get('barangay')
        household = Households.objects.filter(barangay__name=barangay)
        context = {'segment': 'households', 'household': household, 'brgy': brgy}
        html_template = loader.get_template('master/households.html')
        return HttpResponse(html_template.render(context, request))


def add_households(request):
    if request.method == 'GET':
        brgy = Barangay.objects.all().order_by('name')
        context = {'segment': 'survey', 'brgy': brgy}
        html_template = loader.get_template('master/household_add.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        barangay = request.POST.get('barangay')
        address = request.POST.get('address')
        members = request.POST.get('members')
        catholic = request.POST.get('catholic')
        mass_attendance = request.POST.get('mass_attendance')
        not_baptized = request.POST.get('not_baptized')
        not_confirmed = request.POST.get('not_confirmed')
        not_married = request.POST.get('not_married')
        professionals = request.POST.get('professionals')
        stop_highschool = request.POST.get('stop_highschool')
        stop_college = request.POST.get('stop_college')
        living_condition = request.POST.get('living_condition')
        has_lumon = request.POST.get('has_lumon')
        comments = request.POST.get('comments')
        encoder = request.session['login_info'].get('id')
        date = datetime.now()
        user = request.session['login_info'].get('id')

        Households.objects.create(family_name=family_name, barangay_id=barangay, address=address, members=members,
                                catholic=catholic, mass_attendance=mass_attendance, not_baptized=not_baptized,
                                not_confirmed=not_confirmed, not_married=not_married, professionals=professionals,
                                stop_highschool=stop_highschool, stop_college=stop_college, has_lumon=has_lumon,
                                living_condition=living_condition, comments=comments, encoder_id=encoder)

        # update population
        Barangay.objects.filter(id=barangay).update(population=F('population')+members, catholic=F('catholic')+catholic,
                                                    not_baptized=F('not_baptized')+not_baptized, not_married=F('not_married')+not_married,
                                                    professionals=F('professionals')+professionals, stop_highschool=F('stop_highschool')+stop_highschool,
                                                    stop_college=F('stop_college')+stop_college, not_confirmed=F('not_confirmed')+not_confirmed)

        if Records.objects.filter(date=date).exists():
            Records.objects.filter(date=date).update(user=user, no_of_survey=F('no_of_survey')+1)
            msg = "Your work has been saved"
            messages.success(request, f'{msg}')
            return redirect('/add_households/')
        else:
            Records.objects.create(date=date, user=user, no_of_survey=1)
            msg = "Your work has been saved"
            messages.success(request, f'{msg}')
            return redirect('/add_households/')


def edit_households(request, nid):
    query = Households.objects.get(id=nid)
    if request.method == 'GET':
        context = {'segment': 'households', 'query': query}
        return render(request, 'master/household_edit.html', context)
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        barangay = request.POST.get('barangay')
        hec = request.POST.get('hec')
        address = request.POST.get('address')
        members = request.POST.get('members')
        catholic = request.POST.get('catholic')
        mass_attendance = request.POST.get('mass_attendance')
        not_baptized = request.POST.get('not_baptized')
        not_confirmed = request.POST.get('not_confirmed')
        not_married = request.POST.get('not_married')
        professionals = request.POST.get('professionals')
        stop_highschool = request.POST.get('stop_highschool')
        stop_college = request.POST.get('stop_college')
        living_condition = request.POST.get('living_condition')
        has_lumon = request.POST.get('has_lumon')
        comments = request.POST.get('comments')
        encoder = request.session['login_info'].get('id')
        date = datetime.now()
        brgy = Barangay.objects.get(name=barangay, location=hec)

        # minus last value
        Barangay.objects.filter(id=brgy.id).update(population=(F('population') - query.members),
                                                   catholic=(F('catholic') - query.catholic),
                                                   not_baptized=(F('not_baptized') - query.not_baptized),
                                                   not_married=(F('not_married') - query.not_married),
                                                   professionals=(F('professionals') - query.professionals),
                                                   stop_highschool=(F('stop_highschool') - query.stop_highschool),
                                                   stop_college=(F('stop_college') - query.stop_college),
                                                   not_confirmed=(F('not_confirmed') - query.not_confirmed))

        # update value
        Barangay.objects.filter(id=brgy.id).update(population=F('population') + members,
                                                   catholic=F('catholic') + catholic,
                                                   not_baptized=F('not_baptized') + not_baptized,
                                                   not_married=F('not_married') + not_married,
                                                   professionals=F('professionals') + professionals,
                                                   stop_highschool=F('stop_highschool') + stop_highschool,
                                                   stop_college=F('stop_college') + stop_college,
                                                   not_confirmed=F('not_confirmed') + not_confirmed)

        Households.objects.filter(id=nid).update(family_name=family_name, barangay_id=brgy.id, address=address, members=members,
                                                 catholic=catholic, mass_attendance=mass_attendance, not_baptized=not_baptized,
                                                 not_confirmed=not_confirmed, not_married=not_married, professionals=professionals,
                                                 stop_highschool=stop_highschool, stop_college=stop_college, has_lumon=has_lumon,
                                                 living_condition=living_condition, comments=comments, encoder_id=encoder)

        msg = "Your work has been saved"
        messages.success(request, f'{msg}')
        return redirect(f'/household/{nid}/view/')


def view_household(request, nid):
    if request.method == 'GET':
        query = Households.objects.get(id=nid)
        lumon = Lumon.objects.filter(households=nid)
        context = {'query': query, 'lumon': lumon, 'segment': 'households'}
        return render(request, 'master/household_view.html', context)


def approval_householdList(request):
    brgy = Barangay.objects.all().values('name').distinct()
    household = Households.objects.filter(approved_by__isnull=True)
    context = {'segment': 'approvals', 'household': household, 'brgy': brgy}
    return render(request, 'master/households.html', context)


def bulkapprove_household(request):
    if request.method == 'POST':
        object_ids = request.POST.getlist('object_ids')
        admin = request.session['login_info'].get('id')
        date = datetime.today()
        for obj_id in object_ids:
            Households.objects.filter(id=obj_id).update(approved_by=admin, approved_date=date)
        msg = "Your work has been saved"
        messages.success(request, f'{msg}')
        return redirect('/household/approval/list/')


def approve_household(request, nid):
    if request.method == 'GET':
        query = Households.objects.get(id=nid)
        context = {'segment': 'approvals', 'query': query}
        return render(request, 'master/household_approval.html', context)
    if request.method == 'POST':
        admin = request.session['login_info'].get('id')
        date = datetime.today()
        Households.objects.filter(id=nid).update(approved_by=admin, approved_date=date)
        msg = "Your work has been saved"
        messages.success(request, f'{msg}')
        return redirect('/household/approval/list/')


def export_household(request, nid):
    house = Households.objects.get(id=nid)
    doc = DocxTemplate("apps/households/word_templates/Household.docx")

    data = {
        'family_name': house.family_name,
        'barangay': house.barangay.name,
        'address': house.address,
        'members': house.members,
        'catholic': house.catholic,
        'mass_attendance': house.mass_attendance,
        'not_married': house.not_married,
        'not_baptized': house.not_baptized,
        'not_confirmed': house.not_confirmed,
        'professionals': house.professionals,
        'stop_highschool': house.stop_highschool,
        'stop_college': house.stop_college,
        'living_condition': house.living_condition,
        'comments': house.comments,
    }

    doc.render(data)
    doc.save(f'C:\\Users\\EonBotz 5\\Downloads\\{house.family_name}.docx')
    msg = "Check "
    messages.success(request, f'{msg}')
    return redirect('/households/')


def view_householdLumon(request, nid):
    query = Lumon.objects.get(id=nid)
    return render(request, 'master/lumon_view.html', {'query': query})


def csv_household(request):
    household = Households.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Household1.csv"'
    writer = csv.writer(response)
    writer.writerow(['Family Name', 'Members', 'HAS Lumon', 'Catholic Residence', 'Mass Attendance', 'NOT Baptized',
                     'NOT Confirmed', 'NOT Married', 'Professionals', 'STOPPED High School', 'STOPPED College',
                     'Living Condition'])  # header
    for item in household:
        writer.writerow([item.family_name, item.members, item.has_lumon, item.catholic, item.mass_attendance,
                         item.not_baptized, item.not_confirmed, item.not_married, item.professionals,
                         item.stop_highschool, item.stop_college, item.living_condition])  # rows
    return response


def lumon(request):
    if request.method == 'GET':
        brgy = Barangay.objects.all().values('name').distinct()
        lumon = Lumon.objects.all()
        context = {'segment': 'households', 'lumon': lumon, 'brgy': brgy}
        html_template = loader.get_template('master/lumon.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        brgy = Barangay.objects.all().values('name').distinct()
        barangay = request.POST.get('barangay')
        bname = Households.objects.filter(barangay__name=barangay).first()
        lumon = Lumon.objects.filter(households__barangay__name=bname.barangay.name)
        context = {'segment': 'households', 'lumon': lumon, 'brgy': brgy}
        html_template = loader.get_template('master/lumon.html')
        return HttpResponse(html_template.render(context, request))


def add_lumon(request):
    if request.method == 'GET':
        household = Households.objects.filter(has_lumon="Yes")
        context = {'segment': 'households', 'household': household}
        html_template = loader.get_template('master/lumon_add.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        household = Households.objects.get(family_name=request.POST.get('household'))
        members = request.POST.get('members')
        catholic = request.POST.get('catholic')
        mass_attendance = request.POST.get('mass_attendance')
        not_baptized = request.POST.get('not_baptized')
        not_confirmed = request.POST.get('not_confirmed')
        not_married = request.POST.get('not_married')
        professionals = request.POST.get('professionals')
        stop_highschool = request.POST.get('stop_highschool')
        stop_college = request.POST.get('stop_college')
        living_condition = request.POST.get('living_condition')
        comments = request.POST.get('comments')

        Lumon.objects.create(family_name=family_name, members=members, households=household, catholic=catholic,
                                mass_attendance=mass_attendance, not_baptized=not_baptized,
                                not_confirmed=not_confirmed, not_married=not_married, professionals=professionals,
                                stop_highschool=stop_highschool, stop_college=stop_college,
                                living_condition=living_condition, comments=comments)

        # update barangay
        Barangay.objects.filter(id=household.barangay.id).update(population=F('population')+members, catholic=F('catholic')+catholic,
                                                                 not_baptized=F('not_baptized')+not_baptized, not_married=F('not_married')+not_married,
                                                                 professionals=F('professionals')+professionals, stop_highschool=F('stop_highschool')+stop_highschool,
                                                                 stop_college=F('stop_college')+stop_college, not_confirmed=F('not_confirmed')+not_confirmed,
                                                                 lumon=F('lumon')+members)
        return redirect('/lumon/')


def edit_lumon(request, nid):
    query = Lumon.objects.get(id=nid)
    if request.method == 'GET':
        context = {'segment': 'households', 'query': query}
        html_template = loader.get_template('master/lumon_edit.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        family_name = request.POST.get('family_name')
        household = Households.objects.get(family_name=request.POST.get('household'))
        barangay = request.POST.get('barangay')
        hec = request.POST.get('hec')
        members = request.POST.get('members')
        catholic = request.POST.get('catholic')
        mass_attendance = request.POST.get('mass_attendance')
        not_baptized = request.POST.get('not_baptized')
        not_confirmed = request.POST.get('not_confirmed')
        not_married = request.POST.get('not_married')
        professionals = request.POST.get('professionals')
        stop_highschool = request.POST.get('stop_highschool')
        stop_college = request.POST.get('stop_college')
        living_condition = request.POST.get('living_condition')
        comments = request.POST.get('comments')

        brgy = Barangay.objects.filter(name=barangay, location=hec)

        # minus last value
        Barangay.objects.filter(id=brgy.id).update(population=(F('population') - query.members),
                                                   catholic=(F('catholic') - query.catholic),
                                                   not_baptized=(F('not_baptized') - query.not_baptized),
                                                   not_married=(F('not_married') - query.not_married),
                                                   professionals=(F('professionals') - query.professionals),
                                                   stop_highschool=(F('stop_highschool') - query.stop_highschool),
                                                   stop_college=(F('stop_college') - query.stop_college),
                                                   not_confirmed=(F('not_confirmed') - query.not_confirmed))

        # update value
        Barangay.objects.filter(id=brgy.id).update(population=F('population') + members,
                                                   catholic=F('catholic') + catholic,
                                                   not_baptized=F('not_baptized') + not_baptized,
                                                   not_married=F('not_married') + not_married,
                                                   professionals=F('professionals') + professionals,
                                                   stop_highschool=F('stop_highschool') + stop_highschool,
                                                   stop_college=F('stop_college') + stop_college,
                                                   not_confirmed=F('not_confirmed') + not_confirmed)

        Lumon.objects.filter(id=nid).update(family_name=family_name, members=members, households=household,
                                            catholic=catholic, mass_attendance=mass_attendance,
                                            not_baptized=not_baptized, not_confirmed=not_confirmed,
                                            not_married=not_married, professionals=professionals,
                                            stop_highschool=stop_highschool, stop_college=stop_college,
                                            living_condition=living_condition, comments=comments)

        return redirect(f'/household/lumon/{nid}/view/')


def approval_lumonList(request):
    if request.method == 'GET':
        lumon = Lumon.objects.filter(approved_by__isnull=True)
        context = {'segment': 'approvals', 'lumon': lumon}
        return render(request, 'master/lumon.html', context)


def bulkapprove_lumon(request):
    if request.method == 'POST':
        object_ids = request.POST.getlist('object_ids')
        admin = request.session['login_info'].get('id')
        date = datetime.today()
        for obj_id in object_ids:
            Lumon.objects.filter(id=obj_id).update(approved_by=admin, approved_date=date)
        return redirect('/household/lumon/approval/list/')


def approve_lumon(request, nid):
    if request.method == 'GET':
        query = Lumon.objects.get(id=nid)
        context = {'segment': 'approvals', 'query': query}
        return render(request, 'master/lumon_approval.html', context)
    if request.method == 'POST':
        admin = request.session['login_info'].get('id')
        date = datetime.today()
        Lumon.objects.filter(id=nid).update(approved_by=admin, approved_date=date)
        return redirect('/household/lumon/approval/list/')


def export_lumon(request, nid):
    house = Lumon.objects.get(id=nid)
    doc = DocxTemplate("apps/households/word_templates/Lumon.docx")

    data = {
        'family_name': house.family_name,
        'barangay': house.households.barangay.name,
        'address': house.households.address,
        'members': house.members,
        'catholic': house.catholic,
        'mass_attendance': house.mass_attendance,
        'not_married': house.not_married,
        'not_baptized': house.not_baptized,
        'not_confirmed': house.not_confirmed,
        'professionals': house.professionals,
        'stop_highschool': house.stop_highschool,
        'stop_college': house.stop_college,
        'living_condition': house.living_condition,
        'comments': house.comments,
    }

    doc.render(data)
    doc.save(f'C:\\Users\\EonBotz 5\\Downloads\\{house.family_name}.docx')
    return redirect('/lumon/')


def csv_lumon(request):
    lumon = Lumon.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Lumon1.csv"'
    writer = csv.writer(response)
    writer.writerow(['Family Name', 'Members', 'Catholic Residence', 'Mass Attendance', 'NOT Baptized', 'NOT Confirmed',
                     'NOT Married', 'Professionals', 'STOPPED High School', 'STOPPED College', 'Living Condition'])  # header
    for item in lumon:
        writer.writerow([item.family_name, item.members, item.catholic, item.mass_attendance, item.not_baptized,
                         item.not_confirmed, item.not_married, item.professionals, item.stop_highschool,
                         item.stop_college, item.living_condition])  # rows
    return response
