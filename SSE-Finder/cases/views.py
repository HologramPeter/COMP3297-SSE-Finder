
from django.shortcuts import render, redirect
from django.http import HttpResponse
from cases.models import Infector, Event, Attendance
from cases.get import retrive_Data
import datetime as dt

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

# return error message if record already exists
def create_attendance(infector, event_attended, description):
    record = Attendance.objects.filter(infector=infector, event_attended=event_attended)
    # prevent submission if duplicate record
    if (record.exists()):
        return 'This attendance record already exists!'
    is_infected = check_infected(infector, event_attended)
    is_infector = check_infector(infector, event_attended)
    attendance = Attendance.objects.create(infector=infector, event_attended=event_attended, description=description, is_infected=is_infected, is_infector=is_infector)
    return 'Attendance record added successfully.'

# ----- create views here ------ #
# homepage
def index_detail(request):
    return render(request, 'cases/home.html')

# view for adding attendance records
def event_detail(request, case_number):
    # prevent access if case number doesn't exist
    if (not Infector.objects.filter(case_number=case_number).exists()):
        context = {'msg':'Case number not found!'}
        return render(request, 'cases/ok.html', context)

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
        return render(request, 'cases/event.html', ctx)

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
        context = {'msg': create_attendance(infector, event, description)}
        event.is_SSE = check_SSE(event)
        event.save()
        return render(request, 'cases/ok.html', context)

# view for when coordinate retrieval fails
def confirm_detail(request):
    if request.method == 'GET':
        return render(request, 'cases/confirm.html')
    elif request.method == 'POST':
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
        infector = Infector.objects.get(case_number=case_number)
        event = create_event(venue_name, venue_location, date_of_event, [])
        context = {'msg': create_attendance(infector, event, description)}

        # update SSE's
        event.is_SSE = check_SSE(event)
        event.save()
        return render(request, 'cases/ok.html', context)

# view for adding new case
def case_detail(request):
    if request.method == 'GET':
        return render(request, 'cases/case.html')
    elif request.method == 'POST':
        case_number = request.POST.get('case_number')
        person_name = request.POST.get('person_name')
        document_number = request.POST.get('document_number')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_onset = request.POST.get('date_of_onset')
        date_of_confirmation = request.POST.get('date_of_confirmation')

        # check for duplicate
        if (Infector.objects.filter(case_number=case_number).exists()):
            context = {'msg':'Record with case number ' + case_number + ' already exists!'}
            return render(request, 'cases/ok.html', context)

        Infector.objects.create(case_number=case_number, person_name=person_name, document_number=document_number, date_of_birth=date_of_birth, date_of_onset=date_of_onset, date_of_confirmation= date_of_confirmation)
        context = {'msg': 'Record added successfully'}
        return render(request, 'cases/ok.html', context)

# for showing list of all SSE's
def show_sse(request):
    if request.method == 'GET':
        return render(request, 'cases/sse_form.html')
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        events = Event.objects.filter(is_SSE=True).order_by('-date_of_event').filter(date_of_event__range=[start_date, end_date])
        context = {'start_date':start_date, 'end_date':end_date, 'events':events}
        return render(request, 'cases/sse.html', context)
