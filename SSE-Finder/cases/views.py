from django.shortcuts import render, redirect
from django.http import HttpResponse
from cases.models import Infector, Event, Attendance
from cases.get import retrive_Data

# PETER FINISH THESE 3 FUNCTIONS (can move them to other files)
def check_SSE(event):
    # if more than 6 attendance are mapped to this event and have infected=true, set SSE to true, else false
    return False

def check_infected(infector, event):
    return False

def check_infector(infector, event):
    return False


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
# homepage?
def index_detail(request):
    return render(request, 'cases/event.html')

# view for adding attendance records
def event_detail(request, case_number):
    if request.method == 'GET':
        return render(request, 'cases/event.html')

    if request.method == 'POST':
        venue_name = request.POST.get('venue_name')
        venue_location = request.POST.get('venue_location')
        date_of_event = request.POST.get('date_of_event')
        description = request.POST.get('description')

        # prevent submission if case number doesn't exist
        if (not Infector.objects.filter(case_number=case_number).exists()):
            context = {'msg':'Case number not found!'}
            return render(request, 'cases/ok.html', context)

        infector = Infector.objects.get(case_number=case_number)
        # TODO: prevent submission if event date not within 14 days of onset of symptom date
        # TODO: prevent submission if event date is after date_of_confirmation

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
        return render(request, 'cases/ok.html', context)

# view for adding new case
def case_detail(request):
    if request.method == 'GET':
        return render(request, 'cases/case.html')
    elif request.method == 'POST':
        # TODO: prevent submission if date_of_confirmation is earlier than date_of_onset
        # TODO: add some html form validation
        case_number = request.POST.get('case_number')
        person_name = request.POST.get('person_name')
        document_number = request.POST.get('document_number')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_onset = request.POST.get('date_of_onset')
        date_of_confirmation = request.POST.get('date_of_confirmation')
        temp = Infector.objects.create(case_number=case_number, person_name=person_name, document_number=document_number, date_of_birth=date_of_birth, date_of_onset=date_of_onset, date_of_confirmation= date_of_confirmation)
        return render(request, 'cases/case.html')
