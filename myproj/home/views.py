from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, PasswordReset,SetPassword
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.

class HomeView(View):
    def get(self, request):
        context={'user':request.user}
        return render(request, 'home/home.html',context)

def register_user(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful.")
            return redirect(reverse('finapp:main_view'))
        messages.error(request, "Unsuccessful registration. Invalid information.")
        #form=RegisterForm(request.POST)
        return render(request, 'registration/register.html',context={"form":form})
    form = RegisterForm()
    return render(request, 'registration/register.html',context={"form":form})

def password_reset(request):

    if request.method == "POST":
        form=PasswordReset(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            if User.objects.filter(email=email).exists():
                # send email
                send_mail(
                        "Password Reset for My Amazing Stocks",
                        message="",
                        html_message='Click on this <a href="http://localhost:8000/home/set-password/?q={random_string}">link</a> to reset your password.',
                        from_email="from@example.com",
                        recipient_list=["to@example.com"],
                        fail_silently=False,
                )
                
        return render(request,'registration/password-reset-done.html')
             
            
            

    form = PasswordReset()
    return render(request,'registration/password-reset.html',context={"form":form})


def set_password(request):
    form = SetPassword()
    return render(request,'registration/set-password.html',context={"form":form})