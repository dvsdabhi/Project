import email
import re
from django.shortcuts import render,redirect
from .models import *
from random import randrange,choices
from django.conf import settings
from django.core.mail import send_mail
from myapp import models as m

from transporter.models import Transporter

# Create your views here.

def registers(request):
    if request.method == 'POST' :
        try:
            Transporter.objects.get(email=request.POST['email'])
            msg = 'Your Email Is Already Exits'
            return render(request,'registers.html',{msg:'msg'})
        except:
            if request.POST['password'] == request.POST['confirmpassword']:
                global temps
                otp = randrange(1000,9999) 
                temps ={
                    'username' : request.POST['username'],
                    'email' : request.POST['email'],
                    'address' : request.POST['address'],
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'],
                    # 'pic' : request.POST['pic'],
                    'otp' : otp
                }
                subject = 'Building Materials Otp Verify'
                message = f'Hello User your OTP is : {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otps.html',{'otp':otp})
            else:
                msg = 'Your Password And Confirmpassword Does Not Match'
                return render(request,'registers.html',{'msg' : msg})
    return render(request,'registers.html')

def otps(request):
    if request.method == 'POST':
        if request.POST['otp'] == request.POST['uotp']:
            global temps
            Transporter.objects.create(
                username = temps['username'],
                email = temps['email'],
                address = temps['address'],
                mobile = temps['mobile'],
                password = temps['password'],
                # pic = temps['pic'],
            )
            msg = 'User Created'
            del temps
            return render(request,'registers.html',{'msg' : msg})
        else:
            msg = 'Otp Does Not Match'
            return render(request,'otps.html',{'msg' : msg,'otp' : request.POST['otp']})
    return render(request,'otps.html')



def logins(request):
    if request.method == 'POST':
        try:
            tid = Transporter.objects.get(email=request.POST['email'])
            if request.POST['password'] == tid.password:
                request.session['email'] = request.POST['email']
                return render(request,'homes.html',{'tid':tid})
            else:
                return render(request,'logins.html',{'msg' : 'Incorrect Password'})
        except:
            msg = 'First Create Your Account'
            return render(request,'logins.html',{'msg': msg})
    return render(request,'logins.html')


def homes(request):
    try:
        tid = Transporter.objects.get(email=request.session['email'])
        return render(request,'homes.html',{'tid':tid})
    except:
        return render(request,'homes.html')

def logouts(request):
    del request.session['email']
    return render(request,'logins.html')

def forgot_passwords(request):
    if request.POST:
        try:
            tid=Transporter.objects.get(email=request.POST['email'])
            s = 'QWERTYUIOPLKJHGFDSAqwertyuioplkjhgfdsa1236547889'
            pw = ''.join(choices(s,k=8))
            subject = 'Ecomm Reset title'
            message = f"""Hello {tid.username}!!, 
            Your old password is : {tid.password}
            Your New Password is : {pw}

            **Please Login with New Password"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            tid.password = pw
            tid.save()
            return render(request,'logins.html',{'msg':'New password is sent on your email'})
        except:
            return render(request,'forgot-password.html',{'msg':'Email is not register'})
    return render(request,'forgot-password.html')


def profiles(request):
    tid = Transporter.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirmpassword']:
            tid.username = request.POST['username']
            tid.mobile = request.POST['mobile']
            tid.password = request.POST['password']
            tid.address = request.POST['address']
            tid.save()
            return redirect('profiles')
        else:
            return render(request,'profiles.html',{'msg':'Password And Confirmpassword Does Not Match','tid':tid})
    return render(request,'profiles.html',{'tid':tid})

def view_orders(request):
    tid = Transporter.objects.get(email=request.session['email'])
    buys = m.Buy.objects.all()
    select = False
    if request.method == 'POST':
        select = request.POST['search']
        if select == 'pending':
            select = False
        else:
            select = True
    return render(request,'view-orders.html',{'tid':tid,'buys':buys,'select':select})


def complete_dels(request,pk):
    email = m.User.objects.all()
    buy = m.Buy.objects.get(id=pk)
    buy.status = True
    buy.save()
    subject = 'Building Materials Order Delivery'
    message = f'Hello User your Order Successfully deliverd'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [buy.uid.email]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('view-orders')