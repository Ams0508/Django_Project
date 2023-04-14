#from django.contrib import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models as md
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from . import encryption_api
from cryptography.fernet import Fernet
from django.http import JsonResponse
import time
from datetime import datetime, timedelta
from jwt.exceptions import DecodeError, ExpiredSignatureError
import jwt

curl=settings.CURRENT_URL
dt=time.strftime("%d %B %Y - %H:%M:%S %p" )

def sessioncheckmysite_middleware(get_response):
	def middleware(request):
		if request.path=='/home/' or request.path=='/about/' or request.path=='/service/' or request.path=='dashboard/' or request.path=='/login/' or request.path=='/register/':
			request.session["semail"]=None
			request.session["srole"]=None
			response=get_response(request)
		else:
			response=get_response(request)            
		return response
	return middleware


def home(request):
    print(dt)
    return HttpResponse("U r 8 home")

def about(request):
    return HttpResponse("U r 8 about")

def service(request):
    return HttpResponse("U r 8 service")

# Jwt_Token verifying API
def verify_jwt(encoded_jwt):
    secret = settings.SECRET_KEY  
    try:  
        decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=['HS256'],verify=True)  
        print(decoded_jwt)  
        response= HttpResponse(status=200) 
    except jwt.exceptions.InvalidSignatureError: 
        print("Invalid signature.")
        response= HttpResponse(status=401)
    except jwt.exceptions.ExpiredSignatureError:
        print("Token has expired.")
        response= HttpResponse(status=404)
    except DecodeError:
        print("Invalid signature.")
        response= HttpResponse(status=401)
    return response

def dashboard(request):
    if request.method=="GET":
        # Get the JWT token from the request cookies.
        encoded_jwt = request.COOKIES.get('my_tc')
        print(encoded_jwt)
        # Verify the JWT token.
        res = verify_jwt(encoded_jwt)
        print(res)
        if res.status_code == 200:
            all_data = md.F.objects.all().values()
            for data in all_data:
                print("________________________________")
                for k,v in data.items():
                    print(k," : ",v)
            return HttpResponse({"all_data":all_data},"U r 8 Dashboard")
        elif res.status_code == 401:
            return HttpResponse({"error_Invalid_token": "Invalid token"})
        else:
            return HttpResponse({"error_Expired_token": "token expired"})


# JWT_TOKEN Creating API
def jwt_token(email,password):
    header = {"alg": "HS256",  "typ": "JWT"}  
    payload = {"name": email, "password": password, "exp": int(time.time() + timedelta(minutes=1).total_seconds())}  
    secret = settings.SECRET_KEY  
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)  
    print(encoded_jwt)
    return encoded_jwt



@csrf_exempt
def login(request):
    if request.method == "GET":
       if request.GET.get("email")!=None:
        database=md.F.objects.filter(email=em,password=pwd).values('email','password')
        msg=request.GET.get("email")
       else:
        msg="Unknow Request"
       return HttpResponse({'msg':msg},"U  r 8 login")
    else:    
        em=request.POST.get('email')
        pwd=request.POST.get('password')
        data=md.F.objects.filter(email=em).values('email','password','role')
        if len(data)>0:
            if data[0]['email']==em:
                decrypted_password = encryption_api.decrypt_password(data[0]['password'])
                if decrypted_password==pwd:
                    # to store the session
                    request.session["semail"]=data[0]['email']
                    request.session["srole"]=data[0]['role']

                    if data[0]['role']=='admin':
                        token=jwt_token(em,pwd)
                        #res=verify_jwt(token)
                        msg="Login successful for admin"
                        print(msg)   
                        #to store cookies
                        response = HttpResponse('ADMINNNN',{"token":token,'status':200})
                        response.set_cookie('my_cookie',em,3600*12)
                        response.set_cookie('my_tc',token,3600*1)
                        return response
                    else:
                        token=jwt_token(em,pwd)
                        #res=verify_jwt(token)
                        msg="Login successful for user"

                        # to store cookies
                        response = HttpResponse('USERRRR',{"token":token,'status':200})
                        response.set_cookie('my_cookie',em,3600*12)
                        response.set_cookie('my_tc',token,3600*1)
                        print(msg)
                        return response
                else:
                    msg="Wrong password"
                    print(msg)
                    return HttpResponse("Wrong password")
            else:
                msg="Email not found, please check, given email is correct"
                print(msg)
        else:
            msg="not registered yet, check email"
            print(msg)
            return HttpResponse({'msg':msg},"U r 8 login")

#If you want to use in-built authentication for login purposes, here authenticate is in-built functionality.
'''
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("login Successfull")
        else:
            return HttpResponse("Invalid credentials")
    else:
        return HttpResponse("U r 8 login")
'''

@csrf_exempt
def register(request):
    if request.method == "GET":
        return HttpResponse("GET request won't work here")
    else:
        name=request.POST.get("name")               
        mobile=request.POST.get("mobile")
        email=request.POST.get("email")
        passw=request.POST.get("password")
        cpassw=request.POST.get("cpassword")
        city=request.POST.get("city")
        enc_pwd=encryption_api.encrypt_password(passw)
        enc_pwd=str(enc_pwd,'utf8')
        upload_data=md.F(name=name,email=email,mobile=mobile,dt='dt',role='user',password=enc_pwd,cpassword=cpassw,city=city)
        db_data = md.F.objects.values_list('email', flat=True)
        flag=0
        for i in db_data:
            if i!=upload_data.email:
                flag=1
            else:
                flag=0
                break
        if flag==1:
            if passw==cpassw or passw is cpassw:
                upload_data.save()
                msg="Registered Successfully"
                return HttpResponse(msg,"OKAYtemplate")
            else:
                msg="Passwords does not matched"
                return HttpResponse(msg,"U r 8 Register")
        else:
            msg="Email already registered"
            return HttpResponse(msg,"U r 8 Register")