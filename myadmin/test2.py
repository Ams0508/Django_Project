l=[1,2,3,4,5,6,7]

#descending order :
'''
for i in range(len(l)):
    for j in range(i,len(l)):
        if l[i]<l[j]:
            l[i],l[j]=l[j],l[i]
print(l)
'''

# reverse of list :
'''
for i in range(len(l)//2):
    n=l[len(l)-i-1] 
    l[len(l)-i-1]=l[i]
    l[i]=n
print(l)
'''

# fibonacci series :
'''
f=0
s=1
print(f,end=",")
for i in range(1,10):
    print(s,end=", ")
    l=s+f
    f=s
    s=l
    #print("values : ",f,s)
'''

# maximum value :
'''
max=l[0]
for i in range(0,len(l)):
    if l[i]>max:
        max=l[i]
print(max)
'''
# Decorators :

def pikachu(power):
    print("pika..pika")
    def inner(self):
        print("inner functionality adding")
        value=power(self)
        print("called after function call")
        return value
    return inner
@pikachu
def pokemon(text):
    print("pikaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    return text

print(pokemon('pokemon'))





