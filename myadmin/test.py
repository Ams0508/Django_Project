# method overriding
'''class A():
    def show(self):
        print("class A")
    def display(self):
        print("Display class A")
class B(A):
    def show(self):
        print("class B")
    def display(self):
        print("Display class A")
class C(B,A):
    def showw(self):
        print("class C")
    def display(self):
        print("Display class c")
objA=A()
objB=B()
objC=C()
#objA.show()
objC.show()
'''

# method overloading cannot be acheived in python so we have to use 
# None and conditional statements instead.
class example():
    def show(self,name=None,age=None):
        if age!=None and name!=None:
            print("Name and age",name,age)
        elif name!=None:
            print("Name",name)
        else:
            print("Age",age) 
    # def show(self,name,age,city=None):
    #     print("show @")
    # def show(self,name,age,city):
    #     print("show 3")
obj=example()
obj.show("doctors",12)

