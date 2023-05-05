from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from home.models import RecyclerAmount, WasteAmount
from django.views.decorators.csrf import csrf_exempt



@login_required
def home(request):
    if request.method == 'GET':
        # return render(request, 'home.html')
        if request.user.role == User.CUSTOMER:
            return redirect('smartbin')
        elif request.user.role == User.COLLECTION_AGENT:
            return redirect('list_booking')
        elif request.user.role == User.MUNICIPALITY:
            return redirect('list_booking')
        elif request.user.role == User.RECYCLER:
            return redirect('list_recycler_booking')
        elif request.user.role == User.ADMIN:
            return redirect('list_municipalities')



@login_required
@csrf_exempt
def set_waste_amount(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        waste_amount = WasteAmount.objects.get(municipality_id=request.user.id)
        context = {'title': 'Set Amount', 'waste_amount': waste_amount}
        return render(request, 'set_waste_amount.html', context)
    if request.method == 'POST':
        amount = request.POST['waste_amount']
        waste_amount = WasteAmount.objects.get(municipality_id=request.user.id)
        waste_amount.amount = amount
        waste_amount.save()
        return redirect('set_waste_amount')

@login_required
@csrf_exempt
def set_recycler_amount(request):
    if not (request.user.role == User.RECYCLER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        recycler_amount = RecyclerAmount.objects.get(recycler_id=request.user.id)
        context = {'title': 'Set Amount','recycler_amount':recycler_amount}
        return render(request, 'set_recycler_amount.html', context)
    if request.method == 'POST':
        paper_amount = request.POST['paper_amount']
        metal_amount = request.POST['metal_amount']
        agent_amount = request.POST['agent_amount']
        recycler_amount = RecyclerAmount.objects.get(recycler_id=request.user.id)
        recycler_amount.paper_amount=paper_amount
        recycler_amount.metal_amount=metal_amount
        recycler_amount.agent_amount=agent_amount
        recycler_amount.save()
        return redirect('set_recycler_amount')
