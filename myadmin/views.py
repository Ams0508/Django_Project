from django.shortcuts import render,redirect
from . import views
from django.http import HttpResponse
from mysite import settings
from django.views.decorators.csrf import csrf_exempt
curl=settings.CURRENT_URL
from mysite.views import *

# this middleware checks if the user is loggedin or just a fake login 
def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path=='/myadmin/':    
            if request.session['semail']==None or request.session['srole']!="admin":
                response=redirect(curl+'login/')
            else:
                response=get_response(request)
        else:
            response=get_response(request)            
        return response
    return middleware   

@csrf_exempt
def adminhome(request):
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
    return HttpResponse("Admin Home")