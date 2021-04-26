from django.shortcuts import render

# Create your views here.
def index_detail(request):
    return render(request, 'cases/event.html')

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
        return render(request, 'cases/event.html')