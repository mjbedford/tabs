
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

from.models import Tab, UserProfile, Favourite

import re


# login page
# uses django authenticate to chek is user exists and password is correct
# if correct forwars to main page
# if not correct displays a message to the user and redisplays the login page
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

# signup page 
# displays fileds for user credentials, username, email, password
# checks if password is of the right format
# user enters password twice, check is password matches
# regex check to see if password is strong enough
# is any of checks fail display message 
# if all is good saves the user in the django User database
# sets default security questions in profile
#
# checks if the request from the browser is a POST, if not displays empty form
# if it is a POST then processes the form data to create new user
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
        myuser.profile.securityQuestion2= 'To be set by user'
        myuser.profile.securityQuestion3 = 'To be set by user'
        myuser.profile.save()
        messages.success( request, "Your Account has been created")
        user = authenticate(username=username, password=pass1)
        auth_login(request,user)
        messages.success(request, "Your account has been created")
        context = {'newuser': myuser}
        return redirect('/mytabs/qualityoflife', context)
        #return render(request, "mytabs/qualityoflife.html", context)
        
    return render(request, "mytabs/signup.html")

# Account page
def account(request):
    u = User.objects.get(id=request.user.id)
    profile = u.profile
    context = {'profile': profile}
    if request.method=='POST':
        gs1 = request.POST.get('gs1')
        gs2 = request.POST.get('gs2')
        gs3 = request.POST.get('gs3')
        exps1 = request.POST.get('exps1')
        print(gs1)
        print(gs2)
        print(gs3)
        print(exps1)

        u.profile.genre1 = gs1
        u.profile.genre2 = gs2
        u.profile.genre3 = gs3
        u.profile.experienceLevel = exps1

        u.profile.save()
    return render(request, "mytabs/account.html", context)

# Main details page
def detail(request):
    return render(request, "mytabs/detail.html")

# password reset page
# allows user to reset password if one security question answer is corrrect
# uses the same password format checks as signup   
def passwordReset(request, name):
    print(name)
    # get current user from django database
    u = User.objects.get(username=name)
    # get security Q&As from user profile
    vsecq = {"option":[{"key": 1, "string": u.profile.securityQuestion1},
                         {"key": 2, "string": u.profile.securityQuestion2},
                         {"key": 3, "string": u.profile.securityQuestion3}]}
    
    secq = {1:{"key": 1, "string": u.profile.securityQuestion1},
            2: {"key": 2, "string": u.profile.securityQuestion2},
            3: {"key": 3, "string": u.profile.securityQuestion3}}
    seca = {1:{"key": 1, "string": u.profile.securityAnswer1},
            2: {"key": 2, "string": u.profile.securityAnswer2},
            3: {"key": 3, "string": u.profile.securityAnswer3}}
    # process update to passwd
    
    if request.method == "POST":
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        answer=request.POST.get('answer')
        question=request.POST.get('squestions')
        # check if answer to security question is correct
        if seca[int(question)]["string"].lower() == answer.lower() :
            print("GTG")
        else:
            messages.error(request, "Fail!", extra_tags="usererror")
            return redirect( "/mytabs/")
        # check if passwords match
        if pass1 != pass2:
            messages.error(request, "Password do not match!", extra_tags="usererror")
            return redirect( "/mytabs/")
        # set pssword strength pattern 
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        # test strength
        strength = re.match(pattern, pass1)
        if strength == None:
            messages.error(request, "Password not strong enough!", extra_tags="usererror")
            return redirect( "/mytabs/")
        # get current user  
        mUser  = User.objects.get(username=name)
        # update password
        mUser.set_password(pass1)
        # save user 
        mUser.save()
        return redirect( "/mytabs/")
    else:
        #if not post display form
        context = {'resetusername': name, "user": u, "questions": vsecq}
        return render(request, "mytabs/passwordReset.html", context)

# Quality of Life page
def qualityoflife(request ):
    # get user and security Q&A from authencation
    u = User.objects.get(id=request.user.id)
    #u = User.objects.get(username=name)
    profile = u.profile
    print('QofL User')
    print(request.user.id)
    context = {'profile': profile}
    if request.method=='POST':
        gs1 = request.POST.get('gs1')
        gs2 = request.POST.get('gs2')
        gs3 = request.POST.get('gs3')
        exps1 = request.POST.get('exps1')
        print(gs1)
        print(gs2)
        print(gs3)
        print(exps1)
        u.profile.genre1 = gs1
        u.profile.genre2 = gs2
        u.profile.genre3 = gs3
        u.profile.experienceLevel = exps1

        u.profile.save()
        return redirect( "mytabs:securityQuestions")
        #return render(request, "mytabs/securityQuestions.html", context)

    return render(request, "mytabs/qualityoflife.html", context)


# set security questions and answers
def securityQuestions(request):
    # get user and security Q&A from authencation
        print('securityQuestions')
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
            u.profile.securityQuestion2 = request.POST.get("q2")
            u.profile.securityQuestion3 = request.POST.get("q3")
            u.profile.securityAnswer1 = request.POST.get("a1")
            u.profile.securityAnswer2 = request.POST.get("a2")
            u.profile.securityAnswer3 = request.POST.get("a3")
            print(request.POST.get("q1"))
            print(request.POST.get("a1"))
            #save the changes to the user
            # u.profile.securityQuestion1 = 'To be set by user'
            u.profile.save()
            
            print(2)
            u.save()
            return redirect( "mytabs:search")
            #return render(request, "mytabs/account.html")
        else:
        # redirect to acount page
            context = { "user": u,  "answers": seca, "questions": secq}
            return render(request, "mytabs/securityQuestions.html", context)
    
# index page not used
class IndexView(generic.ListView):
    template_name = "mytabs/detail.html"
    context_object_name = "latest_tab_list"
    print('IndexView class called!')
    def get_queryset(self):
        """Return the last five published questions."""
        return Tab.objects.order_by("name")[:5]
    
# detail generic view
class DetailView(generic.DetailView):
    model = Tab
    template_name = "mytabs/detail.html"

# tab search    
def search_tabs(request):
    # lsit for all tabs
    atabs = Tab.objects.all()
    # list of tabs from search
    tabs = Tab.objects.all()
    # filter to get tabs that match search
    myFilter = TabFilter(request.GET, queryset=tabs)
    tabs = myFilter.qs
    print('search tabs')
    # sets context for side bar, context contains the full list and the filtered list to be displayed in sidebar
    context = {"tabs": tabs, "myFilter": myFilter, "atabs": atabs}
    if request.method == "POST":
        print('search_tabs post')
        print(request.POST.get('ctab'))
        ftab = Tab.objects.get(id=request.POST.get('ctab'))
        if ftab != None:
            print(ftab.id)  
            u = User.objects.get(id=request.user.id)
        print(1)
        # favourite =  Favourite.objects.create(user=u , tabId=ftab)
        print(2)
        # u.favourite.tabId = ftab
        messages.success(request, "This tab has been added to your favourites")
        # u.favourite.save()
    return render(request, "mytabs/detail.html", context)


# not used
def search_tabs2(request):
    atabs = Tab.objects.all()
    tabs = Tab.objects.all()
    myFilter = TabFilter(request.GET, queryset=tabs)
    tabs = myFilter.qs
    print('search tabs 2')
    print(tabs)
    context = {"tabs": tabs, "myFilter": myFilter, "atabs": atabs}
    return render(request, "mytabs/search_results.html", context)
