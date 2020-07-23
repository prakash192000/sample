from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo

# home/root page view 
def index(request):
    return render(request,'index.html',{})

# user logout view
@login_required
def user_logout(request):
    logout(request)
    #deleting session on logout
    try:
      del request.session['username']
    except:
        pass
    return HttpResponseRedirect('index.html')

# view for user registration

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        #data validation
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            #saving user information
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        #empty forms for GET requests
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

#user login view
def user_login(request):
    context={}
    if request.method == 'POST':
        #checking whether login credentials are available
        if not request.POST.get('username') or not request.POST.get('password'):
            return HttpResponseRedirect('index.html')
        name = request.POST.get('username')
        password = request.POST.get('password')

        #verifying credentials
        users = UserProfileInfo.objects.all()
        for i in users:
            if i.phone == name:
                username = i.user.username
                break
        #user authentication
        user = authenticate(username=username, password=password)

        #managing session
        request.session['username'] = user.username
        #user login
        if user:
            if user.is_active:
                login(request,user)
                context = { 
                "name":i.user.username,
                "dob":i.date_of_birth,
                "phone":i.phone,
                "email":i.user.email,
                "passport_num":i.passport_num,
                "image":i.profile_pic
                }
                return render(request,'index.html',context)
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})
