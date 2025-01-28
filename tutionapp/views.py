from django.shortcuts import render,redirect
from tutionapp.models import *
from django.contrib import messages, auth
from django.contrib.auth import login,authenticate
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def loginpage(request):
    return render(request, 'loginpage.html')

def teacher_signup(request):
    return render(request, 'teacher_signup.html')

def student_signup(request):
    return render(request, 'student_signup.html')

def teacher_home(request):
    return render(request, 'teacher_home.html')
def student_home(request):
    return render(request, 'student_home.html')

def admin_home(request):
    #Count of Unapproved Users(status 0)
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request, 'admin_home.html',{'unapproved_count':count})

def admin_approval(request):
    users= CustomUser.objects.filter(~Q(user_type="1")) # negation Q (~Q) - exept user_type=1 

    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request, 'admin_approval.html',{'user_data':users, 'unapproved_count':count})

def approve(request, d):
    usr= CustomUser.objects.get(id=d)
    usr.status = 1
    usr.save()

    if usr.user_type == '2':
        teach = Teacher.objects.get(user=d)
        pwd = str(random.randint(100000, 999999))
        print(pwd)
        usr.set_password(pwd)
        usr.save()

        send_mail(
            'Admin approved', 
            f'Username: {teach.user.username} \nPassword: {pwd} \nEmail: {teach.user.email}', 
            settings.EMAIL_HOST_USER,
            {teach.user.email}
        )
        messages.info(request, 'Teacher approved.')
        return redirect('admin_approval')
    elif usr.user_type == '3':
        stud = Student.objects.get(user=d)
        pwd = str(random.randint(100000, 999999))
        print(pwd)
        usr.set_password(pwd)
        usr.save()

        send_mail(
            'Admin approved the student', 
            f'Username: {stud.user.username} \nPassword: {pwd} \nEmail: {stud.user.email}', 
            settings.EMAIL_HOST_USER,
            {stud.user.email}
        )
        messages.info(request, 'Student approved.')
        return redirect('admin_approval')

    return render(request, 'admin_approval.html')

def disapprove(request,d):
    usr= CustomUser.objects.get(id=d)
    
    if usr.user_type == '2':
        Teacher.objects.filter(user=d).delete()
    elif usr.user_type == '3':    
        Student.objects.filter(user=d).delete()
    send_mail(
            'Admin Disapproved', 
            f'Your Registration Has been Disapproved', 
            settings.EMAIL_HOST_USER,
            {usr.email}
        )
    usr.delete()
    messages.info(request, 'User Disapproved.')
    return redirect('admin_approval')

def add_teacher(request):
    if request.method == 'POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        usrname=request.POST['username']
        age=request.POST['age']
        phone=request.POST['phone']
        email=request.POST['email']
        user_type=request.POST['passw']
        photo=request.FILES.get('photo')
        course=request.POST['course']
        if CustomUser.objects.filter(username=usrname).exists():
            messages.info(request,"Username already exist !, Please Choose another")
            return redirect('teacher_signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request,"Email already exist !, Please Choose another")
            return redirect('teacher_signup')
        else:
            usr=CustomUser.objects.create_user(
                username=usrname,
                first_name=fname,
                last_name=lname,
                email=email,
                user_type=user_type
            )
            usr.save()
            teacher=Teacher(
                user=usr,
                course=course,
                age=age,
                contact_no=phone,
                image=photo
            )
            teacher.save()
            messages.info(request,"Registration Succesfull !, Please wait For Admin approval")
            return redirect('teacher_signup')
    return render(request, 'teacher_signup.html')





def add_student(request):
    if request.method == 'POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        usrname=request.POST['username']
        age=request.POST['age']
        phone=request.POST['phone']
        email=request.POST['email']
        user_type=request.POST['passw']
        photo=request.FILES.get('photo')
        course=request.POST['course']
        if CustomUser.objects.filter(username=usrname).exists():
            messages.info(request,"Username already exist !, Please Choose another")
            return redirect('teacher_signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request,"Email already exist !, Please Choose another")
            return redirect('teacher_signup')
        else:
            usr=CustomUser.objects.create_user(
                username=usrname,
                first_name=fname,
                last_name=lname,
                email=email,
                user_type=user_type
                )
            usr.save()
            stud=Student(
                user=usr,
                course=course,
                age=age,
                contact_no=phone,
                image=photo
            )
            stud.save()
            messages.info(request,"Registration Succesfull !, Please wait For Admin approval")
            return redirect('student_signup')
    return render(request, 'student_signup.html')

def log_in(request):
    if request.method == 'POST':
        usrname=request.POST['username']
        pw=request.POST['password']
        user=authenticate(username=usrname, password=pw)

        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return redirect('admin_home')
            elif user.user_type == '2':
                login(request,user)
                return redirect('teacher_home')
            elif user.user_type == '3':
                login(request,user)
                return redirect('student_home')
        else:
            messages.info(request,"Invalid username or password")
            return redirect('loginpage')
        

def teacher_pw_reset(request):
    return render(request, 'teacher_pw_reset.html')

def teacher_reset(request):
    if request.method =='POST':
        npas=request.POST['new_password']
        cpas=request.POST['confirm_password']
        if npas==cpas:
            if len(npas)< 6 or not any(char.isupper() for char in npas) or not any(char.isdigit() for char in npas) or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in npas):
                messages.error(request,'Password must be at least 6 characters long and contain at least one uppercase letter,one digit, and one special character.')
                return redirect('teacher_pw_reset')
            else:
                usr=request.user.id
                tsr=CustomUser.objects.get(id=usr)
                tsr.password=npas
                tsr.set_password(npas)
                tsr.save()
                messages.info(request,"Password Changed")
                return redirect('teacher_pw_reset')
        else:
            messages.error(request,"New Password and Confirm password must be same !!!")
            return redirect('teacher_pw_reset')


    return redirect('teacher_pw_reset')


def student_pw_reset(request):
    return render(request, 'student_pw_reset.html')

def student_reset(request):
    return render(request, 'student_pw_reset.html')




















@login_required(login_url='loginpage')
def logout(request):
    auth.logout(request)
    messages.success(request, "Logged Out.")
    return redirect('loginpage')