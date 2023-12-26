from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from .EmailBackend import EmailBackend
from django.http import HttpResponse
from admin_app.urls import *
from FacultyApp.urls import *
from StaffApp.urls import *
from StudentApp.urls import * 



# Create your views here.
def signin_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("Admin_Home"))
        elif request.user.user_type == '2':
            return redirect(reverse("Faculty_Home"))
        elif request.user.user_type == '3':
            return redirect(reverse("Staff_Home"))
        else:
            return redirect(reverse("student_home"))
    return render(request,'Login.html')


def signin(request,**kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        # Authenticate
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)

            if user.user_type == '1':
                return redirect(reverse("Admin_Home"))
            elif user.user_type == '2':
                return redirect(reverse("Faculty_Home"))
            elif user.user_type == '3':
                return redirect(reverse("Staff_Home"))
            else:
                return redirect(reverse("Student_Home"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")
    

def signout(request):
    if request.user != None:
        logout(request)
    return redirect("/")
