from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
# Create your views here.
from django_otp.oath import hotp
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
import json
from django.core import serializers
from django import forms
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
from random import randint


# @login_required(login_url='/accounts/login/')
@csrf_exempt
def autocompleteModel(request):
    data = json.loads(request.body)
    print(data,"hdsgfgsdhfhdsg")
    results = []
    search_country = Country.objects.filter(name__istartswith=data['search']).using('world')
    search_city = City.objects.filter(name__istartswith=data['search']).using('world')
    search_language = Countrylanguage.objects.filter(language__istartswith=data['search']).using('world')
    print(search_country)
    for r in search_country:
        results.append(r.name)
    for r in search_city:
        results.append(r.name)
    for r in search_language:
        results.append(r.language)
    print(results)
    # resp = request.REQUEST['callback'] + '(' + json.dumps(results) + ');'
    return JsonResponse(results, safe=False)

@csrf_exempt
def login_sample(request):
    print("in login form")
    return render(request, 'dashboard/login.html')

@login_required(login_url='login/')
@csrf_exempt
def selected_name(request):
    input = request.GET['name']
    options = request.GET['options']
    print(options)
    results_country = []
    results = []
    if options == "0":
        print("in if")
        search_country = Country.objects.filter(name=input).using('world')
        search_city = City.objects.filter(name=input).using('world')
        search_language = Countrylanguage.objects.filter(language=input).using('world')
    else:
        print("in else")
        search_country = Country.objects.filter(name__istartswith=input).using('world')
        search_city = City.objects.filter(name__istartswith=input).using('world')
        search_language = Countrylanguage.objects.filter(language__istartswith=input).using('world')
    for r in search_country:
        results_country.append(r.name)
    for r in search_city:
        results.append(r.name)
    for r in search_language:
        results.append(r.language)
    print(results)
    return render(request, "dashboard/results.html", {"results": results, "results_country": results_country})


@login_required(login_url='/home/login/')
@csrf_exempt
def country_details(request):

    input = request.GET['name']
    country_details = Country.objects.using('world').get(name=input)
    print(country_details)
    return render(request, "dashboard/country_details.html", {"country_details": country_details})


# @login_required(login_url='/home/login/')
def signup(request):
    for counter in range(5):
        print(hotp(key=settings.OTP_SECRET_KEY, counter=counter, digits=6))
    return render(request, "dashboard/index.html")


@login_required(login_url='/home/login/')
@csrf_exempt
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


@csrf_exempt
def signup_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        CustomUser(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], phone_number=data['phone_number']).save()
        print(hotp(key=settings.OTP_SECRET_KEY, counter=1, digits=7))

    return HttpResponse(request.body)


@csrf_exempt
def signup_test(request):
    context = {}
    if request.POST:
        print("in post")
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            context['registration_form'] = form
            print(form.errors)
    else:  # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    print(context)
    return render(request, "dashboard/index.html", context)


@csrf_exempt
def login_test(request):
    context = {}
    if request.POST:
        print("in post")
        print(request.POST)
        email = request.POST['email']
        user = CustomUser.objects.get(email=email)
        login(request, user)
        return redirect('dashboard')
    else:  # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    print(context)
    return render(request, "dashboard/index.html", context)

@csrf_exempt
def send_otp_email(request):
    print("in send otp")
    email = json.loads(request.body)['email']
    print(email)
    n = 6
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    otp = randint(range_start, range_end)
    # try:
    count = CheckOtp.objects.filter(email=email).count()
    print(count)
    if count == 0:
        CheckOtp(email=email, otp=otp).save()

    else:
        CheckOtp.objects.filter(email=email).update(otp=otp)
    # except:
    #     CheckOtp(email=email, otp=otp).save()
    send_mail('OTP', 'Here is the message.'+str(otp), settings.EMAIL_HOST_USER,
              [email], fail_silently=False)
    return HttpResponse("success")


@csrf_exempt
def send_otp_email_registered(request):
    email = json.loads(request.body)['email']
    n = 6
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    otp = randint(range_start, range_end)
    # try:
    count = CheckOtp.objects.filter(email=email).count()
    print(count)
    if count == 1:
        CheckOtp.objects.filter(email=email).update(otp=otp)
        send_mail('OTP', 'Here is the message.' + str(otp), settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
    else:
        return HttpResponse("no")
    return HttpResponse("success")


@csrf_exempt
def validate_otp(request):
    email = json.loads(request.body)['email']
    otp = json.loads(request.body)['otp']
    count = CheckOtp.objects.filter(email=email,otp=otp).count()
    if count == 0:
        return HttpResponse("invalid")
    else:
        return HttpResponse("valid")




@csrf_exempt
def logout(request):
    django_logout(request)
    return redirect('index')

@csrf_exempt
def test(request):
    return render(request, 'dashboard/logout.html')

@csrf_exempt
def check_if_mail_exist(request):
    mail = json.loads(request.body)['email']
    count = CustomUser.objects.filter(email=mail).count()
    print(count)
    return HttpResponse(count)