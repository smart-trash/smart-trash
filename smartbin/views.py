from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from booking.models import Booking
from smartbin.models import SmartBin
from home.models import WasteAmount
from wallet.models import Wallet
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



@login_required
def smartbin(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        smartbin = SmartBin.objects.get(user_id=request.user.id)
        booking = Booking.objects.filter(smartbin_id=smartbin.id).exclude(
            status=Booking.VERIFIED).first()
        waste_amount = WasteAmount.objects.get(
            municipality_id=request.user.municipality_id)
        context = {'title': 'Smart Bin',
                   'smartbin': smartbin, 'booking': booking, 'waste_amount': waste_amount}
        return render(request, 'smartbin.html', context)


@login_required
@csrf_exempt
def link_bin(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        context = {'title': 'Link Bin'}
        return render(request, 'link_bin.html', context)
    if request.method == 'POST':
        bin_id = request.POST['bin_id']
        smartbin = SmartBin.objects.get(user_id=request.user.id)
        smartbin.bin_id = bin_id
        smartbin.fill_status = False
        smartbin.save()
        return redirect('smartbin')

@login_required
@csrf_exempt
def unlink_bin(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        smartbin = SmartBin.objects.get(user_id=request.user.id)
        smartbin.bin_id = None
        smartbin.fill_status=False
        smartbin.save()
        return redirect('smartbin')



@login_required
@csrf_exempt
def smartbin_collect_verify(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        waste_amount = WasteAmount.objects.get(
            municipality_id=request.user.municipality_id)
        wallet = Wallet.objects.get(user_id=request.user.id)
        municipality_wallet = Wallet.objects.get(
            user_id=request.user.municipality_id)
        if wallet.amount >= waste_amount.amount:
            booking = Booking.objects.filter(smartbin__user_id=request.user.id).exclude(
                status=Booking.VERIFIED).first()
            booking.status = Booking.VERIFIED
            booking.save()
            smartbin = SmartBin.objects.get(user_id=request.user.id)
            smartbin.fill_status = False
            smartbin.save()
            wallet.amount -= waste_amount.amount
            wallet.save()
            municipality_wallet.amount += waste_amount.amount
            municipality_wallet.save()
        else:
            messages.error(request, 'Insufficient balance')
        return redirect('smartbin')
