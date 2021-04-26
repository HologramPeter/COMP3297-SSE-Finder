from django.shortcuts import render, redirect
from django.http import HttpResponse
from cases.models import Infector, Event
from cases.get import retrive_Data

def index_detail(request):
    return render(request, 'cases/event.html')

def event_detail(request, case_number):
    if request.method == 'GET':
        return render(request, 'cases/event.html')
    elif request.method == 'POST':
        # return render(request, 'cases/ok.html')
        venue_name = request.POST.get('venue_name')
        venue_location = request.POST.get('venue_location')
        date_of_event = request.POST.get('date_of_event')
        description = request.POST.get('description')
        data = retrive_Data(venue_location)
        if (len(data) == 0):
            #fail to retrive the data for x and y and using sesstion to pass the rest of data
            request.session['case_number'] = case_number
            request.session['venue_name'] = venue_name
            request.session['venue_location'] = venue_location
            request.session['date_of_event'] = date_of_event
            request.session['description'] = description
            return redirect('confirm')
        else:
            #save the data as retrive success
            infector = Infector.objects.get(case_number=case_number)
            temp = Event.objects.create(infector=infector, venue_name=venue_name, venue_location=venue_location, date_of_event=date_of_event, description=description)
            return render(request, 'cases/ok.html')

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
        temp = Event.objects.create(infector=infector, venue_name=venue_name, venue_location=venue_location, date_of_event=date_of_event, description=description)
        return render(request, 'cases/ok.html')

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
        temp = Infector.objects.create(case_number=case_number, person_name=person_name, document_number=document_number, date_of_birth=date_of_birth, date_of_onset=date_of_onset, date_of_confirmation= date_of_confirmation)
        return render(request, 'cases/case.html')
