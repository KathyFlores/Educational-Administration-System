from django.shortcuts import render
from basicInfo.models import account as Account
# Create your views here.
def arrangement(request):
    account_id = request.session['account_id']
    account = Account.objects.get(account_id=account_id)

    return render(request, 'courseArrange/arrangement.html', {'account':account})

def calender(request):
    account_id = request.session['account_id']
    account = Account.objects.get(account_id=account_id)
    return render(request, 'courseArrange/calender.html', {'account':account})

def classroom(request):
    account_id = request.session['account_id']
    account = Account.objects.get(account_id=account_id)
    return render(request, 'courseArrange/classroom.html', {'account':account})