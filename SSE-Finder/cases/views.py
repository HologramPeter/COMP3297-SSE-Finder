from django.shortcuts import render, redirect
from django.http import HttpResponse
from cases.models import Infector, Event, Attendance
from cases.get import retrive_Data
import datetime as dt
from django.contrib.auth.decorators import login_required

#------------------SSE functions---------------------#

def check_SSE(event):
    # if more than 6 attendance are mapped to this event and have infected=true, set SSE to true, else false
    attendance = Attendance.objects.filter(event_attended=event).filter(is_infected=True) #TODO discuss if this is necessary
    return len(attendance)>6

def check_infected(infector, event):
    event_date = dt.datetime.strptime(event.date_of_event,"%Y-%m-%d").date() if (isinstance(event.date_of_event,str)) else event.date_of_event
    date_of_onset = infector.date_of_onset

    easliest_date_of_getting_infected = date_of_onset-dt.timedelta(days=14)
    latest_date_of_getting_infected = date_of_onset-dt.timedelta(days=2)

    is_infected = (event_date >= easliest_date_of_getting_infected) and (event_date <= latest_date_of_getting_infected)

    print(is_infected)
    return is_infected

def check_infector(infector, event):
    event_date = dt.datetime.strptime(event.date_of_event,"%Y-%m-%d").date() if (isinstance(event.date_of_event,str)) else event.date_of_event
    date_of_onset = infector.date_of_onset

    easliest_date_of_infecting = date_of_onset-dt.timedelta(days=3)

    is_infector = (event_date >= easliest_date_of_infecting)

    print(event_date, date_of_onset, easliest_date_of_infecting)
    print(is_infector)
    return is_infector



# ----- record creation functions ------ #

# check if event exists in database already, if not then create a new one and return it
def create_event(venue_name, venue_location, date_of_event, data):
    record = Event.objects.filter(venue_name=venue_name, venue_location=venue_location, date_of_event=date_of_event)
    if (record.exists()):
        event = record[0]
    else:
        event = Event.objects.create(venue_name=venue_name, venue_location=venue_location, date_of_event=date_of_event)
    if (len(data) != 0):
        event.venue_address = data[0]
        event.venue_x_coord = data[1]
        event.venue_y_coord = data[2]
    event.save()
    return event

# return false if record already exists
def create_attendance(infector, event_attended, description):
    record = Attendance.objects.filter(infector=infector, event_attended=event_attended)
    # prevent submission if duplicate record
    if (record.exists()):
        return False
    is_infected = check_infected(infector, event_attended)
    is_infector = check_infector(infector, event_attended)
    attendance = Attendance.objects.create(infector=infector, event_attended=event_attended, description=description, is_infected=is_infected, is_infector=is_infector)
    return True



# ----- create views here ------ #
# homepage
@login_required
def index_view(request):
    return render(request, 'cases/index.html')



# view for looking up case by number
@login_required
def case_lookup_view(request):
    if request.method == 'GET':
        return render(request, 'cases/case_lookup.html')
    if request.method == 'POST':
        case_number = request.POST.get('case_number')
        return redirect('/case/' + case_number)

# view for case
@login_required
def case_view(request, case_number):
    if request.method == 'GET':
        # check for infector
        if (not Infector.objects.filter(case_number=case_number).exists()):
            context = {'msg':'Record with case number ' + str(case_number) + ' does not exist!', 'type':'error_msg'}
            return render(request, 'cases/message.html', context, status=202)

        infector = Infector.objects.filter(case_number=case_number)
        context = {'case_number':case_number, 'infector':infector}

        #check for valid attendance
        if Attendance.objects.filter(infector=infector[0]).exists():
            attendances = Attendance.objects.filter(infector=infector[0])
            context['attendances'] = attendances

        return render(request, 'cases/case.html', context)



# view for adding new case
@login_required
def add_case_view(request):
    if request.method == 'GET':
        return render(request, 'cases/add_case.html')
    elif request.method == 'POST':
        case_number = request.POST.get('case_number')
        person_name = request.POST.get('person_name')
        document_number = request.POST.get('document_number')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_onset = request.POST.get('date_of_onset')
        date_of_confirmation = request.POST.get('date_of_confirmation')

        # check for duplicate
        if Infector.objects.filter(case_number=case_number).exists():
            context = {'msg':'Case with case number ' + case_number + ' already exists!', 'type':'error_msg'}
            return render(request, 'cases/message.html', context, status=202)

        if Infector.objects.filter(document_number=document_number).exists():
            context = {'msg':'Case with document number ' + document_number + ' already exists!', 'type':'error_msg'}
            return render(request, 'cases/message.html', context, status=202)

        Infector.objects.create(case_number=case_number, person_name=person_name, document_number=document_number, date_of_birth=date_of_birth, date_of_onset=date_of_onset, date_of_confirmation= date_of_confirmation)
        context = {'msg': 'Case record added successfully', 'type':'case_success', 'case_number':case_number}
        return render(request, 'cases/message.html', context, status=202)

# view for adding attendance records
@login_required
def add_event_view(request, case_number):
    # prevent access if case number doesn't exist
    if (not Infector.objects.filter(case_number=case_number).exists()):
        context = {'msg':'Case number not found!', 'type':'error_msg'}
        return render(request, 'cases/message.html', context, status=202)

    if request.method == 'GET':
        infector = Infector.objects.get(case_number=case_number)
        print(type(infector.date_of_onset))
        if isinstance(infector.date_of_onset, str):
            date_of_onset = dt.datetime.strptime(infector.date_of_onset,"%Y-%m-%d")
            date_of_onset = date_of_onset-dt.timedelta(days=14)
        else:
            date_of_onset = infector.date_of_onset-dt.timedelta(days=14)
        date_of_confirmation = infector.date_of_confirmation
        
        ctx = {
            'date_of_onset': date_of_onset,
            'date_of_confirmation': date_of_confirmation
        }
        return render(request, 'cases/add_event.html', ctx)

    if request.method == 'POST':
        venue_name = request.POST.get('venue_name')
        venue_location = request.POST.get('venue_location')
        date_of_event = request.POST.get('date_of_event')
        description = request.POST.get('description')

        infector = Infector.objects.get(case_number=case_number)

        data = retrive_Data(venue_location)
        print(data)
        if (len(data) == 0):
            #fail to retrive the data for x and y and using sesstion to pass the rest of data
            request.session['case_number'] = case_number
            request.session['venue_name'] = venue_name
            request.session['venue_location'] = venue_location
            request.session['date_of_event'] = date_of_event
            request.session['description'] = description
            return redirect('confirm')

        event = create_event(venue_name, venue_location, date_of_event, data)
        if (create_attendance(infector, event, description)):
            context = {'msg': 'Attendance record added successfully', 'type':'event_success', 'case_number': case_number}
        else:
            context = {'msg': 'Duplicate: this attendance record already exists!', 'type':'error_msg'}
        event.is_SSE = check_SSE(event)
        event.save()
        return render(request, 'cases/message.html', context, status=202)



#view for sse lookup
@login_required
def sse_lookup_view(request):
    if request.method == 'GET':
        start_date = request.GET.get('startdate')
        end_date = request.GET.get('enddate')

        if start_date == None or end_date == None:
            return render(request, 'cases/sse_lookup.html')

        events = Event.objects.filter(is_SSE=True).order_by('-date_of_event').filter(date_of_event__range=[start_date, end_date])
        context = {'start_date':start_date, 'end_date':end_date, 'events':events}
        return render(request, 'cases/sse_list.html', context)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        return redirect('/ssefinder/?startdate=' + start_date + '&enddate=' + end_date)


#view for sse view
@login_required
def sse_view(request, event_pk):
    if request.method == 'GET':
        if (not Event.objects.filter(pk=event_pk).exists()):
            context = {'msg':'Invalid URL', 'type':'error_msg'}
            return render(request, 'cases/message.html', context, status=202)

        event = Event.objects.get(pk=event_pk)

        infector_pk_list = Attendance.objects.filter(event_attended__pk = event_pk, is_infector = True).values_list('infector_id', flat=True).distinct()
        infected_pk_list = Attendance.objects.filter(event_attended__pk = event_pk, is_infected = True).values_list('infector_id', flat=True).distinct()

        infector_list = Infector.objects.filter(pk__in=infector_pk_list)
        infected_list = Infector.objects.filter(pk__in=infected_pk_list)

        context = {'event':event, 'infector_list':infector_list, 'infected_list':infected_list}
        return render(request, 'cases/sse.html', context)



# view for when coordinate retrieval fails
@login_required
def confirm_detail(request):
    if request.method == 'GET':
        return render(request, 'cases/confirm.html')
    elif request.method == 'POST':
        try:
            case_number = request.session['case_number']
            venue_name = request.session['venue_name']
            venue_location = request.session['venue_location']
            date_of_event = request.session['date_of_event']
            description = request.session['description']
            del request.session['case_number']
            del request.session['venue_name']
            del request.session['venue_location']
            del request.session['date_of_event']
            del request.session['description']
        except:
            context = {'msg': 'Operation not allowed!', 'type':'error_msg'}
            return render(request, 'cases/message.html', context, status=202)
        
        infector = Infector.objects.get(case_number=case_number)
        event = create_event(venue_name, venue_location, date_of_event, [])
        if (create_attendance(infector, event, description)):
            context = {'msg': 'Attendance record added successfully', 'type':'event_success', 'case_number':case_number}
        else:
            context = {'msg': 'Duplicate: this attendance record already exists!', 'type':'error_msg'}
        # update SSE's
        event.is_SSE = check_SSE(event)
        event.save()
        return render(request, 'cases/message.html', context, status=202)

