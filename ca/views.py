from django.shortcuts import render, render_to_response
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


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

def get_user(request):
    current_user = request.get.user
    return current_user

class IndexView(generic.View):
	def get(self, request):
		template_name = 'own/index.html'
		return render(request, template_name, {})

class ProfileCreateView(LoggedInMixin,CreateView):
	model = UserProfile
	template_name = 'own/userprofile_form.html'
	fields = ['name','year', 'mobile_number', 'whatsapp_number', 'college',
			'college_address','postal_address','pincode']
	success_url=reverse_lazy('dashboard')

class PosterUploadView(LoggedInMixin,CreateView):
	model = Poster
	template_name = 'own/poster_form.html'
	fields = ['poster_1','poster_2', 'poster_3', 'poster_4']
	success_url=reverse_lazy('dashboard')


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



class AccountDetailView(LoggedInMixin,ListView):
	template_name = 'own/settings.html'


class ToDoListView(LoggedInMixin,generic.ListView):
	template_name = 'own/to_do_list.html'
	def get_queryset(self):
		pass



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
