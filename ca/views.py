from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from ca.models import UserProfile, MassNotification, UserNotification, Poster
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from ca.forms import ImageUploadForm

class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class NoticeMixin(object):
	def get_context_data(self, **kwargs):
		context = super(NoticeMixin,self).get_context_data(**kwargs)
		context[""] = True
		return context

def get_user(request):
    current_user = request.get.user
    return current_user

class IndexView(generic.View):
	def get(self, request):
		template_name = 'own/index.html'
		return render(request, template_name, {})

class ProfileCreateView(LoggedInMixin,CreateView,):
	model = UserProfile
	template_name = 'own/userprofile_form.html'
	fields = ['name','year', 'mobile_number', 'whatsapp_number', 'college',
			'college_address','postal_address','pincode']
	success_url = reverse_lazy('dashboard')

# class PosterUploadView(LoggedInMixin,CreateView):
# 	model = Poster
# 	template_name = 'own/poster_form.html'
# 	fields = ['poster_1','poster_2', 'poster_3', 'poster_4']
# 	success_url = reverse_lazy('dashboard')
#
def PosterUploadView(request):
	context ={
		'all_msgs' : request.user.massnotification_set.all,
		'user_msgs' : request.user.usernotification_set.all,
		'form' : ImageUploadForm(),
		'poster_count': request.user.poster_set.count()
	}
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES,instance=request.user)
		if form.is_valid():
			m = Poster()
			m.poster = form.cleaned_data['poster']
			m.user = request.user
			m.save()
			return redirect('/dashboard/')
		else:
			return render(request,'own/poster_form.html',context)
	else:
		return render(request,'own/poster_form.html',context)

class DashboardView(LoggedInMixin,generic.View):

	def get(self, request):
		template_name = 'own/dashboard.html'
		return render(request, template_name, {})


@login_required(login_url = "/")
def NotificationsView(request):
	template_name = 'own/notifications.html'
	context ={
		'all_msgs': request.user.massnotification_set.all,
		'user_msgs': request.user.usernotification_set.all,
	}
	return render(request, template_name, context)
#{{ request.user.massnotification_set.count|add:request.user.usernotification_set.count}}


def AccountDetailView(request):
	template_name = 'own/settings.html'
	context = {
	'userprofile' : request.user.userprofile,
	}
	return render(request, template_name, context)

# class AccountDetailView(generic.DetailView):
# 	template_name = 'own/settings.html'
# 	model = UserProfile

class ToDoListView(LoggedInMixin,generic.ListView):
	template_name = 'own/to_do_list.html'
	queryset = MassNotification.objects.all()
	def get_context_data(self, **kwargs):
	# Returns a dictionary representing the template context.
	# The keyword arguments provided will make up the returned context
		context = super(ToDoListView,self).get_context_data(**kwargs)
		context['college_count'] = UserProfile.objects.filter(college="IIT BHU").count()
		#and so on for more models
		return  context



# class LoginRequiredMixin(object):
#     """
#     View mixin which verifies that the user has authenticated.
#     NOTE: This should be the left-most mixin of a view.
#     """
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)




# class NotificationsView(LoginRequiredMixin,generic.ListView):
# 	template_name = 'own/notifications.html'
# 	context_object_name = 'all_msgs'
# 	queryset = MassNotification.objects.all()
#
# 	def get_context_data(self, **kwargs):
# 	# Returns a dictionary representing the template context.
# 	# The keyword arguments provided will make up the returned context
# 		context = super(NotificationsView,self).get_context_data(**kwargs)
# 		context['user_msgs'] = UserNotification.objects.get()
# 		#and so on for more models
# 		return  context
#
# 	login_url = 'account_login'
# 	redirect_field_name = 'redirect_to'
