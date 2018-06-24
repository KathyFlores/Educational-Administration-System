from django.shortcuts import render

# Create your views here.
def arrangement(request):
    return render(request, 'courseArrange/arrangement.html', {})

def calender(request):
    return render(request, 'courseArrange/calender.html', {})

def classroom(request):
    return render(request, 'courseArrange/classroom.html', {})