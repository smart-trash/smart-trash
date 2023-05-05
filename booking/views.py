import json
from accounts.models import User, UserLocation
from booking.models import Booking
from smartbin.models import SmartBin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def booking_create(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        bin_id = body.get('bin_id')
        if SmartBin.objects.filter(bin_id=bin_id).exists():
            smartbin = SmartBin.objects.get(bin_id=bin_id)
            if not Booking.objects.filter(smartbin_id=smartbin.id).exclude(status=Booking.VERIFIED).exists():
                Booking.objects.create(
                    smartbin_id=smartbin.id, status=Booking.PENDING, type=Booking.AUTOMATIC)
                smartbin.fill_status = True
                smartbin.save()
                return JsonResponse(
                    {'status': 'success'},
                    safe=False
                )
        else:
            return JsonResponse(
                {'status': 'failed'},
                safe=False
            )


@login_required
@csrf_exempt

def manual_booking(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        smartbin = SmartBin.objects.get(user_id=request.user.id)
        context={'title':'Manual Booking','smartbin':smartbin}
        return render(request,'manual_booking.html',context)
    if request.method == 'POST':
        smartbin = SmartBin.objects.get(user_id=request.user.id)
        Booking.objects.create(smartbin_id=smartbin.id,
                               status=Booking.PENDING, type=Booking.MANUAL)
        smartbin.fill_status = True
        smartbin.save()
        return redirect('smartbin')


@login_required
@csrf_exempt

def list_booking(request):
    if not (request.user.role == User.COLLECTION_AGENT or request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        if request.user.role == User.MUNICIPALITY:
            bookings = Booking.objects.filter(
                smartbin__user__municipality_id=request.user.id).exclude(status=Booking.VERIFIED)
            context = {'title': 'Tasks', 'bookings': bookings}
        if request.user.role == User.COLLECTION_AGENT:
            status = [Booking.VERIFIED,Booking.COLLECTED]
            bookings = Booking.objects.filter(
                collection_agent_id=request.user.id).exclude(status__in=status )
            book= Booking.objects.filter(
                collection_agent_id=request.user.id).exclude(status__in=status ).first()
            location=UserLocation.objects.filter(user_id=book.smartbin.user_id).first()
            context = {'title': 'List Tasks',
                       'bookings': bookings, 'add_button_name': 'COLLECT', 'add_button_url_name': 'collect','location':location}
        return render(request, 'list_booking.html', context)

@csrf_exempt

def navigate_view(request, location_id):
    location = UserLocation.objects.get(id=location_id)
    return redirect('https://www.google.com/maps/dir/?api=1&destination={0},{1}'.format(location.latitude, location.longitude))


@login_required
@csrf_exempt

def detailed_view(request, booking_id):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        booking = Booking.objects.get(id=booking_id)
        agents = User.objects.filter(
            role=User.COLLECTION_AGENT, municipality_id=request.user.id)
        context = {'title': 'Tasks', 'booking': booking, 'agents': agents}
        return render(request, 'detailed_view.html', context)
    if request.method == 'POST':
        collection_agent = request.POST.get('collection_agent')
        collection_date = request.POST.get('date')
        booking = Booking.objects.get(id=booking_id)
        booking.collection_agent_id = collection_agent
        booking.collection_date = collection_date
        booking.status = Booking.ASSIGNED
        booking.save()
        return redirect('detailed_view', booking_id=booking_id)


@login_required
@csrf_exempt

def collect(request):
    if not (request.user.role == User.COLLECTION_AGENT):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        bin_id=request.GET.get('bin_id')
        context = {'title': 'Collect Garbage','bin_id':bin_id}
        return render(request, 'collect.html', context)
    if request.method == 'POST':
        bin_id = request.POST['bin_id']
        print(bin_id)
        if Booking.objects.filter(smartbin__bin_id=bin_id, collection_agent_id=request.user.id).exclude(status=Booking.VERIFIED).exists():
            booking = Booking.objects.filter(smartbin__bin_id=bin_id, collection_agent_id=request.user.id).exclude(
                status=Booking.VERIFIED).first()
            booking.status = Booking.COLLECTED
            booking.save()
            # user=SmartBin.objects.filter(bin_id=bin_id).first()
            # print('smart',user)
            # located_user=UserLocation.objects.filter(user_id=user.user_id).first()
            # located_user.delete()
            return redirect('list_booking')
        else:
            messages.info(request, 'Invalid Bin ID or already collected')
            return redirect('collect')


@login_required
def booking_history(request):
    if not (request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER or request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        if request.user.role == User.CUSTOMER:
            bookings = Booking.objects.filter(
                smartbin__user_id=request.user.id, status=Booking.VERIFIED)
        elif request.user.role == User.COLLECTION_AGENT:
            bookings = Booking.objects.filter(
                collection_agent_id=request.user.id, status=Booking.VERIFIED)
        elif request.user.role == User.MUNICIPALITY:
            bookings = Booking.objects.filter(
                smartbin__user__municipality_id=request.user.id, status=Booking.VERIFIED)
        context = {'title': 'History', 'bookings': bookings}
        return render(request, 'booking_history.html', context)
