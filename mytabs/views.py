
from django.http import HttpResponse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from mytabs.filters import TabFilter

from.models import Tab, UserProfile

import re

# Create your views here.
# def index(request):
#     return HttpResponse("hello")
def login(request):
     if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST.get('pass1')
        print("username")
        print(username)
        user = authenticate(username=username, password=pass1)

        if user is not None:
            print("Authenticated")
            auth_login(request,user)
            print("logged in")
            # return render(request, "mytabs/index.html")
            return redirect( "mytabs:search")
        else:
            print("Bad Credentials")
            messages.error(request, "Username or Password not correct!", extra_tags="usererror")
            return redirect('/mytabs/')
        

     return render(request, "mytabs/login.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Password do not match!", extra_tags="usererror")
            return HttpResponseRedirect(request.path_info) 
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        strength = re.match(pattern, pass1)
        if strength == None:
            messages.error(request, "Password not strong enough!", extra_tags="usererror")
            return HttpResponseRedirect(request.path_info) 

        myuser = User.objects.create_user(username, email, pass1)

        
        myuser.save()
        profile = UserProfile.objects.create(user=myuser)
        myuser.profile.securityQuestion1 = 'To be set by user'
        myuser.profile.save()
        messages.success( request, "Your Account has been created")
        # messages.error(request, "Username or Password not correct!", extra_tags="usererror")
        return redirect('/mytabs/')

        
    return render(request, "mytabs/signup.html")


def account(request):
    return render(request, "mytabs/account.html")
def detail(request):
    return render(request, "mytabs/detail.html")

    
def passwordReset(request, name):
    print(name)
    u = User.objects.get(username=name)
    
    vsecq = {"option":[{"key": 1, "string": u.profile.securityQuestion1},
                         {"key": 2, "string": u.profile.securityQuestion2},
                         {"key": 3, "string": u.profile.securityQuestion3}]}
    
    secq = {1:{"key": 1, "string": u.profile.securityQuestion1},
            2: {"key": 2, "string": u.profile.securityQuestion2},
            3: {"key": 3, "string": u.profile.securityQuestion3}}
    seca = {1:{"key": 1, "string": u.profile.securityAnswer1},
            2: {"key": 2, "string": u.profile.securityAnswer2},
            3: {"key": 3, "string": u.profile.securityAnswer3}}
    
    if request.method == "POST":
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        answer=request.POST.get('answer')
        question=request.POST.get('squestions')
      
        if seca[int(question)]["string"].lower() == answer.lower() :
            print("GTG")
        else:
            messages.error(request, "Fail!", extra_tags="usererror")
            return redirect( "/mytabs/")
        if pass1 != pass2:
            messages.error(request, "Password do not match!", extra_tags="usererror")
            return redirect( "/mytabs/")
            # return HttpResponseRedirect(request.path_info) 
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        strength = re.match(pattern, pass1)
        if strength == None:
            messages.error(request, "Password not strong enough!", extra_tags="usererror")
            return redirect( "/mytabs/")
            # return HttpResponseRedirect(request.path_info) 
        # print(seca.get(int(question)).string)
        mUser  = User.objects.get(username=name)
        mUser.set_password(pass1)
        
        mUser.save()
        return redirect( "/mytabs/")
    else:
       
        context = {'resetusername': name, "user": u, "questions": vsecq}
        return render(request, "mytabs/passwordReset.html", context)

def qualityoflife(request):
    return render(request, "mytabs/qualityoflife.html")

def securityQuestions(request):
    # get user and security Q&A from authencation
        u = User.objects.get(id=request.user.id)
        secq = {"option":[{"key": 1, "string": u.profile.securityQuestion1},
                         {"key": 2, "string": u.profile.securityQuestion2},
                         {"key": 3, "string": u.profile.securityQuestion3}]}
        seca = {"option":[{"key": 1, "string": u.profile.securityAnswer1},
                         {"key": 2, "string": u.profile.securityAnswer2},
                         {"key": 3, "string": u.profile.securityAnswer3}]}
        
        if request.method == "POST":
        # update security questions
            print("POST")
            # get the updated values from the form via the POST object
            u.profile.securityQuestion1 = request.POST.get("q1")
            u.profile.securityQuestion1 = request.POST.get("q2")
            u.profile.securityQuestion1 = request.POST.get("q3")
            u.profile.securityAnswer1 = request.POST.get("a1")
            u.profile.securityAnswer1 = request.POST.get("a2")
            u.profile.securityAnswer1 = request.POST.get("a3")
            print(request.POST.get("a3"))
            #save the changes to the user
            u.profile.securityQuestion1 = 'To be set by user'
            u.profile.save()
            
            print(2)
            u.save()
            return render(request, "mytabs/account.html")
        else:
        # redirect to acount page
            context = { "user": u,  "answers": seca, "questions": secq}
            return render(request, "mytabs/securityQuestions.html", context)
    

class IndexView(generic.ListView):
    template_name = "mytabs/detail.html"
    context_object_name = "latest_tab_list"
    print('IndexView class called!')
    def get_queryset(self):
        """Return the last five published questions."""
        return Tab.objects.order_by("name")[:5]

class DetailView(generic.DetailView):
    model = Tab
    template_name = "mytabs/detail.html"
    
def search_tabs(request):
    atabs = Tab.objects.all()
    tabs = Tab.objects.all()
    myFilter = TabFilter(request.GET, queryset=tabs)
    tabs = myFilter.qs
    print(1)
    context = {"tabs": tabs, "myFilter": myFilter, "atabs": atabs}
    return render(request, "mytabs/detail.html", context)
def search_tabs2(request):
    atabs = Tab.objects.all()
    tabs = Tab.objects.all()
    myFilter = TabFilter(request.GET, queryset=tabs)
    tabs = myFilter.qs
    print(tabs)
    context = {"tabs": tabs, "myFilter": myFilter, "atabs": atabs}
    return render(request, "mytabs/search_results.html", context)
