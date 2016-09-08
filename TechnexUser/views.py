from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
import json

from TechnexUser.models import TechProfile, UserStatus
from TechnexUser.forms import *

#json.loads will load a json object into a python dict,
# json.dumps will dump a python dict to a json object,

def context_call(request):
    context = {
        'name':request.user.first_name + " " + request.user.last_name,
    }
    return context

#for techusers who want to be a CA.
@login_required(login_url='/login')
def Tech2CA(request):
    template_name = 'technexuser/tech2ca.html'
    u = request.user
    if request.method == "POST":
        form = Tech2CAForm(request.POST)
        if form.is_valid:
            caprofile = form.save(commit=False)
            #saved WhatsApp,col add,postal add, pincode.
            caprofile.user = u
            caprofile.college = u.techprofile.college
            caprofile.mobile_number = u.techprofile.mobile_number
            caprofile.year = u.techprofile.year
            caprofile.save()

            u.userstatus.is_ca = True
            return redirect('/ca/dashboard')

    else:
        ca = request.user.userstatus.is_ca
        if not ca:
            form = Tech2CAForm()
            return render(request,template_name,{'form':form})
        else:#already a CA.
            raise Http404('Not allowed')


def FbView(request):

    '''
    User comming here are already authenticated by fb: either first time login,
    or logging into their technex account with fb.
    for first time ppl,..we have User instance only with first/last name & email.
    '''

    if request.method == "POST":
        #user has submitted the techprofile form. i.e, after fb login and getting FbForm()
        form = FbForm(request.POST)
        if form.is_valid:
            techuser = form.save(commit=False)
            techuser.user = request.user
            techuser.save()

            status = UserStatus.objects.create(user=request.user)
            status.is_techuser = True
            status.save()

            return redirect('/dashboard')
    else:#came here either first time or just loggin in with FB.
        if request.user.is_authenticated:#obviously if came here after FB
            try:
                fb_user = UserStatus.objects.get(user=request.user)
                already_a_user = True
            except:
                already_a_user = False

            if not already_a_user: #first time.
                form = FbForm()
                template_name = 'technexuser/fbregister.html'
                return render(request,template_name,{'form':form})
            else:#trying to log in..userstatus already there..
            #the user is already logged in,.redirect to dashboard.
                return redirect('/dashboard')
        else:#anonymous user..
            raise Http404('Not allowed!')


def IndexView(request):
    template_name = 'technexuser/index.html'
    return render(request,template_name,{})


def RegisterView(request):
    template_name = 'technexuser/registration.html'
    all_colleges = College.objects.all()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        post = request.POST
        if form.is_valid:
            email = post['email']
            try:
                already_a_user = User.objects.get(username=email)
            except:
                already_a_user = None

            if already_a_user is None:
                user = User.objects.create_user(username=email, email=email)
                user.first_name = post['first_name']
                user.last_name = post['last_name']
                password = post['password']
                user.set_password(password)
                user.save()

                techprofile = form.save(commit=False)
                techprofile.college = post.get('college') #not rendered as model in form, #autocomplete
                techprofile.user = user
                techprofile.save()

                status = UserStatus.objects.create(user=user,is_techuser=True)

                new_user = authenticate(username=email, password=password)
                login(request, new_user)

                return redirect('/dashboard')
            else:#already_a_user
                messages.warning(request,'email allready registered! try diffrent email id.',fail_silently=True)
                return render(request,template_name,{'form':form, 'all_colleges':all_colleges})
        else:
            return render(request,template_name,{'form':form, 'all_colleges':all_colleges})
    else:
        return render(request,template_name,{'form':RegisterForm(),'all_colleges':all_colleges})


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
                if user.userstatus.is_techuser == True:
                    return redirect('/dashboard')
                else:
                    return redirect('/ca/dashboard')
            else:
                messages.error(request,'Invalid Credentials',fail_silently=True)
                return render(request,template_name,{'form':form})
        else:
            return render(request,template_name,{'form':form})
    else:
        return render(request,template_name,{'form': LoginForm()})

@login_required(login_url='/login') #not /login/
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def DashboardView(request):
    status = request.user.userstatus #created at the time of techprofile registration.
    if status.is_techuser == True:
        template_name = 'technexuser/dashboard.html'
        context = context_call(request)
        return render(request,template_name,context)
    else:
        #the user hasn't registered for technex.
        return redirect('/register')


@csrf_exempt
def ApiRegisterView(request):
    response_data = {}
    data =json.loads(request.body)
    try:
        form = RegisterForm(data)
        email = data.get('email',None)
        user = User.objects.create_user(username=email, email=email)
        user.first_name = data.get('first_name',None)
        user.last_name = data.get('last_name',None)
        password = data.get('password',None)
        user.set_password(password)
        user.save()

        techprofile = form.save(commit=False)
        techprofile.user = user
        techprofile.save()

        status = UserStatus.objects.create(user=user,is_techuser=True)

        new_user = authenticate(username=email, password=password)
        login(request, new_user)

        response_data['status'] = "Profile created successfully"
        return JsonResponse(response_data)
    except:
        form = RegisterForm(data)
        for field in form:
            if field.errors:
                response_data[field.html_name] = field.errors.as_text()
                response_data['status'] = 'Error in registration'
        return JsonResponse(response_data)

    else:
        response_data['error'] = True
        response_data['status'] = 'invalid request,Post request Please!'
        return JsonResponse(response_data)

@csrf_exempt
def ApiLoginView(request):
    response_data = {}
    data = json.loads(request.body)
    try:
        form = LoginForm(data)
        if form.is_valid:
            email = data.get('email',None)
            password = data.get('password',None)
            user = authenticate(username=email, email=email, password=password)
            if user is not None:
                login(request, user)
                response_data['status'] = 'logged in'
                return JsonResponse(response_data)
            else:
                response_data['error'] = True
                response_data['status'] = 'Invalid Credentials!'
                return JsonResponse(response_data)
    except:
        response_data['error'] = True
        response_data['status'] = "Please Fill the form correctly!"


# def CollegeSearch(request):
#     if request.is_ajax:
#         q = request.GET.get('term', '')
#         print q
#         print request
        # search_qs = College.objects.filter(collegeName__startswith=request.POST.get('search'))
        # results = []
        # for r in search_qs:
        #     json_data = {}
        #     json_data['id'] = r.collegeId
        #     json_data['label'] = r.CollegeName
        #     json_data['value'] = r.CollegeName
        #     results.append(json_data)
        #
        # resp = json.dumps(results)
        # print resp
        # return HttpResponse(resp, content_type='application/json')
