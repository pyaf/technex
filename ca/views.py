from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import requests
import json
import facebook
import re
from ca.models import *
from ca.forms import *
from TechnexUser.models import *

def context_call(request):
    college = request.user.caprofile.college
    ca_college_profile = CAProfile.objects.filter(college=college) #for showing other CAs of one's college.

#will raise an error in  time visit of CA to the dashborad, when the User hasn't  created caprofile
#using ProfileCreateView and trying to visit dashboard
    try:
        ca = request.user.caprofile
    except:
        ca = None

    context = {
            'technexuser_college_count' : TechProfile.objects.filter(college=college).count(),
            'caprofile' : ca,
            'mass_msgs': ca.massnotification_set.all,
            'user_msgs': ca.usernotification_set.filter(mark_read=False),
            'all_user_msgs': ca.usernotification_set.all(),
            'total_msgs': ca.massnotification_set.count() + ca.usernotification_set.filter(mark_read=False).count(),
            'poster_count': ca.poster_set.count(),
            'form' : ImageUploadForm(),
            'techprofiles' : TechProfile.objects.filter(college=college),
            'posters' : Poster.objects.filter(ca=request.user.caprofile),

        }
    return context


@login_required(login_url = "/login")
def notificationsView(request):
    template_name = 'ca/notifications.html'
    context = context_call(request)
    return render(request, template_name, context)

@csrf_exempt
def NoticeBooleanUpdate(request):
    if request.method == "POST" and request.is_ajax():
        msg_id = request.POST.get('msg_id')
        print msg_id
        response_data = {}
        notice = request.user.caprofile.usernotification_set.get(id=msg_id)
        notice.mark_read = True
        notice.save()

        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see":"this is not working"}),
            content_type = "application/json"
        )

class IndexView(generic.View):
    def get(self, request):
        template_name = 'ca/index.html'
        return render(request, template_name, {})

def CARegistrationView(request):
    template_name = 'ca/CARegistration.html'
    context = {
            'all_colleges':College.objects.all(),
            'form' : CARegistrationForm()
    }
    if request.method == "POST":
        post = request.POST
        form = CARegistrationForm(request.POST)
        if form.is_valid():
            email = post['email']
            password1 = post['password1']
            password2 = post['password2']
            if password1 == password2:
                try:
                    already_a_user = User.objects.get(username=email)
                except:# unique user.
                    already_a_user = False

                if not already_a_user:#create new User instance.
                    user = User.objects.create_user(username=email,email=email)
                    user.first_name = post.get('name')
                    user.set_password(password1)
                    user.save()
                    caprofile = CAProfile.objects.create(user=user)
                    try:
                        college = College.objects.get(collegeName=post.get('college'))
                    except:
                        college = College.objects.create(collegeName=post.get('college'))

                    caprofile.college = college
                    caprofile.save()

                    status = UserStatus.objects.create(user=user)
                    #CA by default is to be made ca and techuser.
                    #we will make is_ca and is_techuser after ca profile creation
                    new_user = authenticate(username=email,password=password1)
                    login(request,new_user)

                    return redirect('/ca/profile_registration')

                else:# already a user.
                    messages.warning(request,'email already registered!, if you have already registered for Technex, the link of CA registration is at dashboard',fail_silently=True)
                    return render(request,template_name,{'form':form, 'all_colleges':context['all_colleges']})

            else: #password mismatch
                messages.warning(request,"Passwords didn't match")
                return render(request,template_name,{'form':form,'all_colleges':context['all_colleges']})
        else: #form isn't valid
            return render(request,template_name,{'form':form,'all_colleges':context['all_colleges']})

    else: #not a post request
        return render(request,template_name,context)


@login_required(login_url = "/login")
def ProfileCreateView(request):

    context = {
            'form': ProfileCreationForm(),
    }

    template_name = 'ca/profile_registration.html'
    if request.method == 'POST':
        post = request.POST
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            #User and its CAProfile instance is has already been created in CARegistrationView
            caprofile = CAProfile.objects.get(user=request.user)
            caprofile.year = post.get('year')
            caprofile.mobile_number = post.get('mobile_number')
            caprofile.whatsapp_number = post.get('whatsapp_number')
            caprofile.college_address = post.get('college_address')
            caprofile.postal_address = post.get('postal_address')
            caprofile.save()

            #UserStatus is already created, as the user has signned in currently,.So it is a User n so has UserStatus
            status = UserStatus.objects.get(user=request.user)
            status.is_ca = True
            status.is_techuser = True#every CA has to be made a techuser by default
            status.save()

            messages.success(request, 'Profile set successfully.',fail_silently=True)
            return redirect('/ca/dashboard/')

        else:
            return render(request,template_name,{'form':form})


            # User is registered and currently logged in. If User is registered by allauth(ca/register) then
            # UserStatus obj hasn't been created yet. if User was created at technexUser then userstatus
            # object is created with is_techuser = True.

            #remember login is neccesary for this view. so we have request.user
    else:
        try:
            status = UserStatus.objects.get(user=request.user)
            #status is created at CA Signup,..is_ca n is_techuser is True only when Profile is created
            already_a_User = True
        except:
            already_a_User = False

        if already_a_User:
            if status.is_ca:#profile created
                messages.warning(request, 'You have already created your profile.',fail_silently=True)
                return redirect('/ca/dashboard')

            else: #not is_ca,..serve the caprofile creation form.
                return render(request,template_name,context)


'''
IF THERE'S A LOOP OF BETWEEN DashboardView AND ProfileCreateView--> THE BUG May be IN context_call!!
It might not raise an error and trigger the except in DashboardView-->ProfileCreateView-->>DashboardView and so on!!
###THAT'S WHY TO PREVENT SUCH SITUATION USED try for 'context'.
'''

@login_required(login_url='/login')
def DashboardView(request):
    template_name = 'ca/dashboard.html'
    try:
        profile_done = request.user.userstatus.is_ca
        context = context_call(request)
        return render(request,template_name,context)
    except Exception as e:
        return HttpResponse(e)
        # return redirect('/ca/profile_registration')

@login_required(login_url = "/login")
def PosterUploadView(request):
    template_name = 'ca/poster_form.html'
    context = context_call(request)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.user = request.user
            img.save()
            messages.success(request, 'Poster uploaded successfully.',fail_silently=True)
            return redirect('/ca/dashboard/')
        else:
            return render(request,template_name,context)
    else:
        return render(request,template_name,context)

@login_required(login_url = "/login")
def AllPosterView(request):
    template_name = 'ca/all_posters.html'
    context = context_call(request)
    return render(request,template_name, context)


#{{ request.user.massnotification_set.count|add:request.user.usernotification_set.count}}


@login_required(login_url = "/login")
def AccountDetailView(request):
    template_name = 'ca/settings.html'
    context = context_call(request)
    return render(request, template_name, context)


@login_required(login_url = "/login")
def ToDoListView(request):
    template_name = 'ca/to_do_list.html'
    context = context_call(request)
    return render(request,template_name,context)


@login_required(login_url='/login')
def UpcomingEventsView(request):
    template_name = 'ca/upcoming_events.html'
    context = context_call(request)

    return render(request,template_name,context)
'''
Auto like,comment and share of posts of technex page while checking if post already shared.
limit for sharing number of posts arranged as per the latest.
'''
def auto_likes(request,limit = 2):
    token="EAACEdEose0cBAG4NjT4N71AF1Rv8DwHpFMwBLjpjgSXYeKZBvzqHuIqSyo0LeqSZANrZBrUvp41k0EJPtN3DQQtPTpiF2OKCPnJJJZAFwR2g4LqODG1oeQdHBn6CHlgAi4xOusCKGoPRfxoHK8z686Akd299fyedLIvVXmyypwZDZD"
    graph = facebook.GraphAPI(access_token = token, version= '2.2')
    profile = graph.get_object(id ='225615937462895')
    posts = graph.get_connections(profile['id'],"posts",limit = limit)
    userPosts = graph.get_object("me/feed")
    #print(userPosts['data'])

    links = []
    for userPost in userPosts['data']:
        links.append(userPost['link'])
    #postIds = []
    linksPosted = []
    for post in posts['data']:
        try:
            graph.put_object(post['id'],"likes")
            #postIds.append(post['link'])
            attachment = {
            'link':post['link'],
            'name': 'testName',
            'caption':'testCaption',
            'description':'testDescription',
            'picture':''
            }
            print post['link']
            if post['link'] not in links:
                linksPosted.append(post['link'])
                graph.put_wall_post(message='',attachment = attachment)
            #graph.put_comment(post['id'],message="(Y)")
        except:
            continue
    return HttpResponse(str(linksPosted))

#if user likes the page widout the bug :)
def user_likes_page(page_id, token):
    """
    Returns whether a user likes a page
    """
    url = 'https://graph.facebook.com/me/likes/%s/' % page_id
    parameters = {'access_token': token}
    r = requests.get(url, params = parameters)
    result = json.loads(r.text)
    print r.text
    if result['data']:
        return True
    else:
        return False

def demoCheck(request):
    pageId = '225615937462895'
    token="EAAEaYmywDIABANytfYi7RojZCXh7pX1WTbI1FefjtqhviGKcze89SkyLmyZBCCra94Mk7dbBn2jlewgG43DagbhDmhEUlgI1URR8siLJm4tfligl4FOOzhGHkYZBGk5twErHuog45Mm5p932zM3fhOvTwNUgf3eZA8raeLIuRSOGx1xX6cAS3OdL2YUnuoZBOruE0R1ph9wZDZD"
    if user_likes_page(pageId,token):
        return HttpResponse("liked")
    else:
        return HttpResponse("Not Liked!")

def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'scope':'user_likes,publish_actions', 'client_id': app_id, 'client_secret': app_secret,'redirect_uri':'http://localhost:8000/'}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    print file.text #to test what the FB api responded with
    #result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return file.text

def demofb_id(request):
    print str(request)
    app_id = '461359507257085'
    app_secret = '7be92fe7ee2c2d12cd2351d2a2c0dbb8'
    #token = get_fb_token(app_id, app_secret)
    #facebook.auth_url(app_id,'http://locahost:8000/ca/demofb_id',)
    return render(request,'ca/fblogin.html')
