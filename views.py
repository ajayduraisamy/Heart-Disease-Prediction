from django.shortcuts import redirect, render
from My_Prediction.forms import CustomUserForm
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth import authenticate,login


def home(request):
    return render(request, "my/index.html")

def login_page(request):
     if request.method=='POST':
         name=request.POST.get('username')
         pwd=request.POST.get('password')
         user=authenticate(request,username=name,password=pwd)
         if user is not None:
             login(request,user)
            # message.success(request,"Logged in successfully")
         else:
            # message.error(request,"Invalid user name or password")
             return redirect("/login")
     return render(request, "my/login.html")

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            #message.success(request,"Registration Success You can Login Now..!")
            return redirect('/login')
    return render(request, "my/register.html", {'form': form})



def results(request):
    return render(request, "my/results.html")


def contact(request):
    return render(request, "my/contact.html")

