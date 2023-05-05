from django.http import HttpResponse
from django.shortcuts import render
from accounts.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def help(request):
    if not (request.user.role == User.MUNICIPALITY or request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER or request.user.role == User.RECYCLER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        context={'title':'Help'}
        return render(request,'help.html',context)