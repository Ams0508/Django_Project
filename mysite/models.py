from django.db import models


# class Register(models.Model):
#     uid=models.AutoField(primary_key=True)
#     name=models.CharField(max_length=50,default="unknown")
#     email=models.EmailField(max_length=50,default="unknown")   
#     password=models.CharField(max_length=10,default="unknown")
#     cpassword=models.CharField(max_length=10,default="unknown")
#     mobile=models.CharField(max_length=10,default="unknTrue,blank=True
#     city=models.CharField(max_length=20,default="unknown")

class F(models.Model):
    uid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, default='',null=True)
    email=models.EmailField(max_length=50, default='',null=True)   
    password=models.CharField(max_length=255, default='',null=True)
    cpassword=models.CharField(max_length=10, default='',null=True)
    mobile=models.CharField(max_length=10, default='',null=True)
    dt=models.DateField(auto_now_add=True,null=True)
    role=models.CharField(max_length=10,default='',null=True)
    city=models.CharField(max_length=20, default='',null=True)

 
 

