from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import auth
from access.models import ForgotPassword
from accounts.models import User, CollectionAgent
from home.models import RecyclerAmount
from smartbin.models import SmartBin
from wallet.models import Wallet
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')
@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        content=request.POST['message']
        subject = 'Contact Us - Smartrash'
        message = 'Name: '+first_name+' '+ last_name+'\nEmail: '+email+'\nMessage: '+content
        email_from = 'prolog586@gmail.com'
        recipient_list = ['prolog586@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        return redirect('index')
def customer(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.CUSTOMER:
            return redirect('home')
        else:
            return redirect('customer_login')

@csrf_exempt
def customer_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.CUSTOMER:
            return redirect('home')
        context = {'title': 'Customer Login',
                   'signup_url_name': 'customer_signup', 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.CUSTOMER:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('customer_login')


def agent(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.COLLECTION_AGENT:
            return redirect('home')
        else:
            return redirect('agent_login')

@csrf_exempt
def agent_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.COLLECTION_AGENT:
            return redirect('home')
        context = {'title': 'Agent Login',
                   'signup_url_name': 'agent_signup', 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.COLLECTION_AGENT:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('agent_login')


def municipality(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.MUNICIPALITY:
            return redirect('home')
        else:
            return redirect('municipality_login')

@csrf_exempt
def municipality_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.MUNICIPALITY:
            return redirect('home')
        context = {'title': 'Municipality Login',
                   'signup_url_name': None, 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.MUNICIPALITY:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('municipality_login')


def recycler(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.RECYCLER:
            return redirect('home')
        else:
            return redirect('recycler_login')

@csrf_exempt
def recycler_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.RECYCLER:
            return redirect('home')
        context = {'title': 'Recycler Login',
                   'signup_url_name': None, 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.RECYCLER:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('recycler_login')


def admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.ADMIN:
            return redirect('home')
        else:
            return redirect('admin_login')

@csrf_exempt
def admin_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.ADMIN:
            return redirect('home')
        context = {'title': 'Admin Login',
                   'signup_url_name': None, 'show_forgot_password': False}
        return render(request, 'login.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.ADMIN:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('admin_login')


def logout(request):
    auth.logout(request)
    return redirect('index')

@csrf_exempt
def customer_signup(request):
    if request.method == 'GET':
        municipalities = User.objects.filter(role=User.MUNICIPALITY)
        context = {'title': 'Customer signup',
                   'login_url_name': 'customer_login', 'municipalities': municipalities, 'is_customer_page': True, 'is_agent_page': False, 'is_recycler_page': False}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        house_name = request.POST['house_name']
        place = request.POST['place']
        municipality_id = request.POST['municipality']
        postcode = request.POST['postcode']
        state = request.POST['state']
        country = request.POST['country']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        profile_image = request.FILES['profile_image']
        if not password1 == password2:
            messages.info(request, 'password incorrect')   
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        elif User.objects.filter(phone=phone).exists():
            messages.info(request, 'phone number already registered')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=email,
                                            email=email, phone=phone, housename=house_name, place=place,
                                            municipality_id=municipality_id, postcode=postcode, state=state,
                                            country=country, password=password1, profile_image=profile_image,
                                            role=User.CUSTOMER, is_active=False)
            print(user.id)
            SmartBin.objects.create(user_id=user.id)
            Wallet.objects.create(amount=0, user_id=user.id)
            return redirect('customer_login')
        return redirect('customer_signup')

@csrf_exempt
def agent_signup(request):
    if request.method == 'GET':
        municipalities = User.objects.filter(role=User.MUNICIPALITY)
        context = {'title': 'Agent signup',
                   'login_url_name': 'agent_login', 'municipalities': municipalities, 'is_agent_page': True, 'is_recycler_page': False, 'is_customer_page': False}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        house_name = request.POST['house_name']
        place = request.POST['place']
        municipality_id = request.POST['municipality']
        postcode = request.POST['postcode']
        state = request.POST['state']
        country = request.POST['country']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        aadhaar_number = request.POST['aadhaar']
        license_number = request.POST['license']
        aadhaar_image = request.FILES['aadhaar_pic']
        license_image = request.FILES['license_pic']
        profile_image = request.FILES['profile_image']

        if not password1 == password2:
            messages.info(request, 'password incorrect')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        elif User.objects.filter(phone=phone).exists():
            messages.info(request, 'phone number already registered')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=email,
                                            email=email, phone=phone, housename=house_name, place=place, municipality_id=municipality_id,
                                            postcode=postcode, state=state, country=country, password=password1, profile_image=profile_image, role=User.COLLECTION_AGENT, is_active=False)
            CollectionAgent.objects.create(aadhaar_number=aadhaar_number, license_number=license_number,
                                           aadhaar_image=aadhaar_image, license_image=license_image, user_id=user.id)
            Wallet.objects.create(amount=0, user_id=user.id)
            return redirect('agent_login')
        return redirect('agent_signup')


# def recycler_signup(request):
#     if request.method == 'GET':
#         municipalities = User.objects.filter(role=User.MUNICIPALITY)
#         context = {'title': 'Recycler signup',
#                    'login_url_name': 'recycler_login', 'municipalities': municipalities, 'is_agent_page': False, 'is_recycler_page': True, 'is_customer_page': False}
#         return render(request, 'signup.html', context)
#     if request.method == 'POST':
#         name = request.POST['name']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         building_name = request.POST['building_name']
#         place = request.POST['place']
#         municipality_id = request.POST['municipality']
#         postcode = request.POST['postcode']
#         state = request.POST['state']
#         country = request.POST['country']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if not password1 == password2:
#             messages.info(request, 'password incorrect')
#         elif User.objects.filter(email=email).exists():
#             messages.info(request, 'email taken')
#         elif User.objects.filter(phone=phone).exists():
#             messages.info(request, 'phone number already registered')
#         else:
#             recycler = User.objects.create_user(first_name=name, username=email,
#                                             email=email, phone=phone, housename=building_name, place=place,
#                                             municipality_id=municipality_id, postcode=postcode, state=state,
#                                             country=country, password=password1, role=User.RECYCLER)
#             Wallet.objects.create(amount=0, user_id=recycler.id)
#             RecyclerAmount.objects.create(recycler_id=recycler.id)
#             return redirect('recycler_login')
#         return redirect('recycler_signup')

@csrf_exempt
def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')
    if request.method == 'POST':
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            messages.info(request, 'email not registered')
        else:
            reset_id = str(uuid.uuid4())
            ForgotPassword.objects.create(id=reset_id, email=email)
            reset_url = settings.SERVER_URL+'/reset-password/'+reset_id
            subject = 'Reset Password - Smartrash'
            message = ' Click below link to reset password ' + reset_url
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('index')
        return redirect('forgot_password')

@csrf_exempt
def reset_password(request, reset_id):
    if request.method == 'GET':
        if not ForgotPassword.objects.filter(id=reset_id).exists():
            return HttpResponse('Unauthorized', status=401)
        return render(request, 'reset_password.html')
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if not password == confirm_password:
            messages.info(request, 'password incorrect')
        else:
            forgot_password = ForgotPassword.objects.get(id=reset_id)
            user = User.objects.get(email=forgot_password.email)
            user.set_password(password)
            user.save()
            forgot_password.delete()
            return redirect('index')
        return redirect('reset_password')
