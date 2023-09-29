from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse

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