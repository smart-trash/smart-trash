from django.shortcuts import render,HttpResponse
from accounts.models import  User
from wallet.models import Wallet
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def wallet(request):
    if not (request.user.role == User.MUNICIPALITY or request.user.role == User.CUSTOMER or request.user.role == User.RECYCLER or request.user.role == User.COLLECTION_AGENT):
        return HttpResponse('Unauthorized', status=401)
    if request.method=='GET':
        wallet=Wallet.objects.get(user_id=request.user.id)
        context={'title': 'Wallet','wallet':wallet}
        return render(request,'wallet.html',context)

@login_required
@csrf_exempt
def add_wallet(request):
    if not (request.user.role == User.MUNICIPALITY or request.user.role == User.CUSTOMER or request.user.role == User.RECYCLER or request.user.role == User.COLLECTION_AGENT):
        return HttpResponse('Unauthorized', status=401)
    if request.method=='POST':
        amount=request.POST['amount']
        wallet=Wallet.objects.get(user_id=request.user.id)
        wallet.amount += float(amount)
        wallet.save()
        return JsonResponse(
            {'amount':wallet.amount,},
            safe=False
        )
       

    

