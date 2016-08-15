from django.shortcuts import render, render_to_response
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from ca.models import UserProfile
from allauth import app_settings as allauth_app_settings

class IndexView(generic.ListView):
	template_name = 'own/index.html'

	def get_queryset(self):
		pass

class ProfileCreateView(CreateView):
	model = UserProfile
	template_name = 'own/userprofile_form.html'
	fields = ['name','year', 'mobile_number', 'whatsapp_number', 'college',
			'college_address','postal_address','pincode']
	success_url=reverse_lazy('dashboard')

class DashboardView(generic.View):

	def get(self, request):
		template_name = 'own/dashboard.html'
		return render(request, template_name, {})

class SettingsView(generic.View):
	def get(self, request):
		template_name = 'own/settings.html'
		return render(request, template_name,{})
