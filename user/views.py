from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mysite import settings
from mysite.views import *
curl=settings.CURRENT_URL

def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path=='/user/':    
            if request.session['semail']==None or request.session['srole']!="user":
                response=redirect(curl+'login/')
            else:
                response=get_response(request)
        else:
            response=get_response(request)            
        return response
    return middleware  


@csrf_exempt
def userhome(request):
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
    return HttpResponse('User home')

