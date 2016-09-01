from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from TechnexUser.models import TechProfile, UserStatus
from TechnexUser.forms import LoginForm, RegisterForm


def context_call(request):
    context = {
        'name':request.user.first_name + " " + request.user.last_name,
    }

    return context

def IndexView(request):
    template_name = 'technexuser/index.html'
    return render(request,template_name,{})

def RegisterView(request):
    template_name = 'technexuser/registration.html'
    data = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        post = request.POST
        if form.is_valid:
            email = post['email']
            username = post['email']
            user = User.objects.create_user(username=username, email=email)
            user.first_name = post['first_name']
            user.last_name = post['last_name']
            password = post['password']
            user.set_password(password)
            user.save()
            techprofile = form.save(commit=False)
            techprofile.user = user
            techprofile.save()
            status = UserStatus.objects.create(user=user,is_techuser=True)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            data['status'] = 'OK'
            return JsonResponse(data)
        else:
            data['error'] = True
            data['status'] = 'Form Not Validated'
            return JsonResponse(data)
    else:
        data['error'] = True
        data['status'] = 'Invalid Request'
        return JsonResponse(data)


def LoginView(request):
    template_name = 'technexuser/login.html'
    if request.method == "POST":
        post = request.POST
        form = LoginForm(post)
        if form.is_valid:
            email = post['email']
            password = post['password']
            user = authenticate(username=email, email=email, password=password)
            if user is not None:
                login(request,user)
                return redirect('/dashboard')
            else:
                data['status'] = 'OK'
            return JsonResponse(data)
        else:
            data['error'] = True
            data['status'] = 'Form Not Validated'
            return JsonResponse(data)
    else:
        data['error'] = True
        data['status'] = 'Invalid Request'
        return JsonResponse(data)

@login_required(login_url='/login') #not /login/
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def DashboardView(request):
    template_name = 'technexuser/dashboard.html'
    context = context_call(request)
    return render(request,template_name,context)
