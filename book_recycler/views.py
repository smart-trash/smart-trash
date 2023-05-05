from django.shortcuts import render, redirect, HttpResponse
from accounts.models import User
from book_recycler.models import RecyclerBooking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import RecyclerAmount
from wallet.models import Wallet
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def recycler_booking(request):
    if request.method == 'GET':
        if User.objects.filter(municipality_id=request.user.municipality_id, role=User.RECYCLER).exists():
            is_recycler_available = True
            recycler = User.objects.get(role=User.RECYCLER, municipality_id=request.user.municipality_id)
            recycler_amount=RecyclerAmount.objects.get(recycler_id=recycler.id)
            recycler_booking = RecyclerBooking.objects.filter(user_id=request.user.id).exclude(
            status=RecyclerBooking.VERIFIED).first()
            if RecyclerBooking.objects.filter(user_id=request.user.id).exclude(status=RecyclerBooking.VERIFIED).exists():
                allow_new_booking = False
            else:
                allow_new_booking = True
            context = {'title': 'Book Recycler', 'allow_new_booking': allow_new_booking,
                   'recycler_booking': recycler_booking,'recycler_amount':recycler_amount,'is_recycler_available': is_recycler_available}
        else:
            is_recycler_available = False
            context = {'title': 'Book Recycler','is_recycler_available': is_recycler_available}
       
       
        return render(request, 'recycler_booking.html', context)
    if request.method == 'POST':
        paper_waste = request.POST['paper_waste']
        metal_waste = request.POST['metal_waste']
        recycler = User.objects.get(
            role=User.RECYCLER, municipality_id=request.user.municipality_id)
        RecyclerBooking.objects.create(paper_waste=paper_waste, metal_waste=metal_waste,
                                       status=RecyclerBooking.PENDING, user_id=request.user.id, recycler_id=recycler.id)
        return redirect('recycler_booking')

@csrf_exempt

def list_recycler_booking(request):
    if not (request.user.role == User.RECYCLER or request.user.role == User.COLLECTION_AGENT):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        if request.user.role == User.RECYCLER:
            recycler_bookings = RecyclerBooking.objects.filter(
                recycler_id=request.user.id).exclude(status=RecyclerBooking.VERIFIED)
            recycler_amount=RecyclerAmount.objects.get(recycler_id=request.user.id)
            for recycler_booking in recycler_bookings:
                recycler_booking.total_price_for_waste = recycler_booking.paper_waste*recycler_amount.paper_amount + recycler_amount.metal_amount*recycler_booking.metal_waste
            context = {'title': 'List Tasks',
                       'recycler_bookings': recycler_bookings,'recycler_amount':recycler_amount}

        if request.user.role == User.COLLECTION_AGENT:
            recycler_bookings = RecyclerBooking.objects.filter(
                collection_agent_id=request.user.id).exclude(status=RecyclerBooking.VERIFIED)
            context = {'title': 'Recycler Tasks',
                       'recycler_bookings': recycler_bookings}
        return render(request, 'list_recycler_booking.html', context)


@login_required
@csrf_exempt

def recycler_booking_detailed_view(request, recycler_booking_id):
    if not (request.user.role == User.RECYCLER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        recycler_booking = RecyclerBooking.objects.get(id=recycler_booking_id)
        agents = User.objects.filter(
            role=User.COLLECTION_AGENT, municipality_id=request.user.municipality_id)
        context = {'title': 'Detailed View',
                   'recycler_booking': recycler_booking, 'agents': agents}
        return render(request, 'recycler_booking_detailed_view.html', context)
    if request.method == 'POST':
        collection_agent = request.POST.get('collection_agent')
        collection_date = request.POST.get('date')
        recycler_booking = RecyclerBooking.objects.get(id=recycler_booking_id)
        recycler_booking.collection_agent_id = collection_agent
        recycler_booking.collection_date = collection_date
        recycler_booking.status = RecyclerBooking.ASSIGNED
        recycler_booking.save()
        return redirect('recycler_booking_detailed_view', recycler_booking_id=recycler_booking_id)

@csrf_exempt

def recycler_collect(request, recycler_booking_id):
    if not (request.user.role == User.COLLECTION_AGENT):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        recycler_booking = RecyclerBooking.objects.get(id=recycler_booking_id)
        recycler_booking.status = RecyclerBooking.COLLECTED
        recycler_booking.save()
        return redirect('list_recycler_booking')

@csrf_exempt

def recycler_verify(request, recycler_booking_id):
    if not (request.user.role == User.RECYCLER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        recycler_booking = RecyclerBooking.objects.get(id=recycler_booking_id)
        recycler_amount = RecyclerAmount.objects.get(
            recycler_id=request.user.id)
        recycler_wallet = Wallet.objects.get(user_id=request.user.id)

        total_price_for_waste = recycler_booking.paper_waste*recycler_amount.paper_amount + recycler_amount.metal_amount*recycler_booking.metal_waste
        total_price_for_recycler = total_price_for_waste+recycler_amount.agent_amount

        if recycler_wallet.amount > total_price_for_recycler:
            user_wallet = Wallet.objects.get(user_id=recycler_booking.user_id)
            agent_wallet = Wallet.objects.get(
                user_id=recycler_booking.collection_agent_id)
            recycler_booking.status = RecyclerBooking.VERIFIED
            recycler_booking.save()
            recycler_wallet.amount -= total_price_for_recycler
            user_wallet.amount += total_price_for_waste
            agent_wallet.amount += recycler_amount.agent_amount
            recycler_wallet.save()
            user_wallet.save()
            agent_wallet.save()
        else:
            messages.info(request, 'Insufficient money in wallet')
        return redirect('list_recycler_booking')

@csrf_exempt

def recycler_history(request):
    if not (request.user.role == User.RECYCLER or request.user.role == User.CUSTOMER or request.user.role == User.COLLECTION_AGENT):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        if request.user.role == User.CUSTOMER:
            recycler_bookings = RecyclerBooking.objects.filter(
                user_id=request.user.id, status=RecyclerBooking.VERIFIED)
        elif request.user.role == User.COLLECTION_AGENT:
            recycler_bookings = RecyclerBooking.objects.filter(
                collection_agent_id=request.user.id, status=RecyclerBooking.VERIFIED)
        elif request.user.role == User.RECYCLER:
            recycler_bookings = RecyclerBooking.objects.filter(
                recycler_id=request.user.id, status=RecyclerBooking.VERIFIED)
        context = {'title': 'Recycler History',
                   'recycler_bookings': recycler_bookings}
        return render(request, 'recycler_booking_history.html', context)
