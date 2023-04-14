enc_pwd=b'password'
enc_pwd=str(enc_pwd,'utf8')
print(type(enc_pwd),enc_pwd,type(enc_pwd))

_______________________________________________________________



from django.test import TestCase

# Create your tests here.

import time
from datetime import timedelta
from django.http import HttpResponse
import jwt
from django.conf import settings

# Verify JWT token
def verify_jwt(encoded_jwt):
    secret = settings.SECRET_KEY  
    try:  
        decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=['HS256'],verify=True)  
        print(decoded_jwt)  
        return decoded_jwt
    except jwt.exceptions.InvalidSignatureError: 
        print("Invalid signature.")
        return None
    except jwt.exceptions.ExpiredSignatureError:
        print("Token has expired.")
        return None

# Generate JWT token
def generate_jwt(email, password):
    header = {"alg": "HS256",  "typ": "JWT"}  
    payload = {"name": email, "password": password, "exp": int(time.time() + timedelta(minutes=1).total_seconds())}  
    secret = settings.SECRET_KEY  
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)  
    print(encoded_jwt)
    return encoded_jwt

# Refresh JWT token
def refresh_jwt(encoded_jwt):
    decoded_jwt = verify_jwt(encoded_jwt)
    if decoded_jwt is None:
        return None
    email = decoded_jwt['name']
    password = decoded_jwt['password']
    new_token = generate_jwt(email, password)
    return new_token

# Dashboard view
def dashboard(request):
    if request.method=="GET":
        # Get the JWT token from the request cookies.
        encoded_jwt = request.COOKIES.get('my_tc')
        print(encoded_jwt)
        decoded_jwt = verify_jwt(encoded_jwt)
        if decoded_jwt is not None:
            all_data = md.F.objects.all().values()
            for data in all_data:
                print("________________________________")
                for k,v in data.items():
                    print(k," : ",v)
            return HttpResponse({"all_data":all_data},"U r 8 Dashboard")
        else:
            # Try to refresh the token
            new_token = refresh_jwt(encoded_jwt)
            if new_token is not None:
                response = HttpResponse(status=200)
                response.set_cookie('my_tc', new_token)
                return response
            else:
                return HttpResponse({"error_Expired_token": "token e