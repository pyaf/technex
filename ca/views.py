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

import json

from ca.models import *
from ca.forms import ImageUploadForm, ProfileCreationForm
from TechnexUser.models import *

def context_call(request):
    college = request.user.caprofile.college
    ca_college_profile = CAProfile.objects.filter(college=college) #AWESOMMMMMENESS AMPLIFIED :D
    context = {
            'college_count' : User.objects.filter(caprofile=ca_college_profile).count(),
            'userprofile' : request.user.caprofile,
            'all_msgs': request.user.massnotification_set.all,
            'user_msgs': request.user.usernotification_set.filter(mark_read=False),
            'poster_count': request.user.poster_set.count(),
            'form' : ImageUploadForm(),
            'techprofiles' : TechProfile.objects.filter(college=college),
            'posters' : Poster.objects.filter(user=request.user),
        }
    return context

@csrf_exempt
def NoticeBooleanUpdate(request):
    if request.method == "POST" and request.is_ajax():
        msg_id = request.POST.get('msg_id')
        response_data = {}
        notice = request.user.usernotification_set.get(id=msg_id)
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

@login_required(login_url='/login')
def DashboardView(request):
    template_name = 'ca/dashboard.html'
    try:
        profile_done = request.user.userstatus.is_ca
        context = context_call(request)
        return render(request,template_name,context)
    except:
        return redirect('/ca/profile_registration')

@login_required(login_url = "/login")
def ProfileCreateView(request):

    profile_context = {
            'form': ProfileCreationForm(),
    }

    template_name = 'ca/profile_registration.html'
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            caprofile = form.save(commit=False)
            caprofile.user = request.user
            caprofile.user.first_name = request.POST['first_name']
            caprofile.user.last_name = request.POST['last_name']
            caprofile.save()
            caprofile.user.save() #in order to save the first_name and last_name of current user.
            status = UserStatus.objects.get_or_create(user=request.user)[0]
            status.is_ca = True
            status.save()

            messages.success(request, 'Profile set successfully.',fail_silently=True)
            return redirect('/ca/dashboard/')

        else:
            return render(request,template_name,{'form':form})

        '''
User is registered and currently logged in. If User is registered by allauth(ca/register) then
UserStatus obj hasn't been created yet. if User was created at technexUser then userstatus object is created
with is_techuser = True.

        '''

    else:
        status, created_right_now = UserStatus.objects.get_or_create(user=request.user)

        if not created_right_now: # allready created userstatus

            if status.is_ca: # user has already created caprofile at ca portal.
                messages.warning(request, 'You have already created your profile.',fail_silently=True)
                return redirect('/ca/dashboard')

            else: #A techuser wants to be CA. serve the ca profile form.
                return render(request,template_name,profile_context)

        else: #ca has just registered on ca portal through allauth, serve the caprofile form.
            return render(request,template_name,profile_context)


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


@login_required(login_url = "/login")
def NotificationsView(request):
    template_name = 'ca/notifications.html'
    context = context_call(request)
    return render(request, template_name, context)
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
