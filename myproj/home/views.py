from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, PasswordReset,SetPassword
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from finapp.models import UserMeta
import random
import string

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
                user = User.objects.get(email=email)
                letters = string.ascii_lowercase
                random_string = ''.join(random.choice(letters) for i in range(30))
                # UserMeta.objects.create(user=user,random_pass_string=random_string)

                #create or update user_meta table based on user_id
                UserMeta.objects.update_or_create(
                                    user=user,
                                    defaults={"random_pass_string": random_string},
                                )
                # send email
                # using mailtrap for testing send email. Later on, have to implement own email server in production.
                # To change email settings in settings.py change following parameters:
                # EMAIL_HOST,EMAIL_PORT, EMAIL_USE_SSL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

                send_mail(
                        "Password Reset for My Amazing Stocks",
                        message="",
                        html_message=f'Hi {user.first_name} {user.last_name},<br> <p>Click on this <a href="http://localhost:8000/home/set-password/?email={email}&q={random_string}">link</a> to reset your password.</p> <p>Thank you.</p><p>My Amazing Stock Team</p>',
                        from_email="from@example.com",
                        recipient_list=["to@example.com"],
                        fail_silently=False,
                )
                
                return render(request,'registration/password-reset-done.html',context={"next":"inbox"})
             
    form = PasswordReset()
    return render(request,'registration/password-reset.html',context={"form":form})


def set_password(request):
    message = ""
    if(request.method == "POST"):
        form = SetPassword(request.POST)
        if form.is_valid() == False:
              return render(request, 'registration/set-password.html',context={"form":form})
        
        password1 = request.POST.get('password1')
        email = request.GET.get('email')
        random_string = request.GET.get('q')
      
        user = User.objects.get(email=email)
        query_string = user.usermeta.random_pass_string
        #checking if email and string matches to database's email and string
        if(random_string != query_string):
              message="Something went wrong. Please retry with link in email"
              return render(request, 'registration/set-password.html',context={"form":form,"next":message})      
                
         #change password
        user.set_password(password1)
        user.save()
        #delete user meta after password changed
        UserMeta.objects.filter(user=user).delete()
        return render(request,"registration/password-reset-done.html",context={"next":"done"})
                            
            
    form = SetPassword()
    context = {"form":form,"next":message}
    return render(request,'registration/set-password.html',context=context)