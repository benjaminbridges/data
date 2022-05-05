from django.shortcuts import render, redirect
from .decorators import unauthenticted_user, allowed_users
from data.models import Profile, Survey
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def index(request):
    return redirect('mysurveys')
    # return render(request, "website/index.html")


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def info(request):
    return render(request, "website/info.html")


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def contact(request):
    return render(request, "website/contact.html")


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def myprofile(request):
    userdetail = request.user.profile.user
    userprofile = Profile.objects.get(user=request.user)
    surveylist = Survey.objects.filter(
        surveyentity__surveybreakdown__surveyinstance__profile__id=userprofile.id).distinct()
    return render(request, "website/myprofile.html",
                  {'userprofile': userprofile, 'userdetail': userdetail, 'surveylist': surveylist})


# - User Registration and loging - #


# @unauthenticted_user
# def registerpage(request):
#    form = CreateUserForm()
#    if request.method == "POST":
#        form = CreateUserForm(request.POST)
#        if form.is_valid():
#            obj = form.save(commit=False)
#            obj.username = obj.email
#            form.save()
#            first_name = form.cleaned_data.get('first_name')
#            messages.success(request, 'Account was created for ' + first_name)
#            return redirect("loginpage")
#    context = {'form':form}
#    return render(request, 'website/registerpage.html', context)

@unauthenticted_user
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'No account matches Username or Password')
    return render(request, 'website/loginpage.html')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def logoutUser(request):
    logout(request)
    return redirect('loginpage')
