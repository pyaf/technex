from django.conf.urls import url, include

from django.contrib import admin
from ca.views import (IndexView,ProfileCreateView,
					DashboardView,SettingsView)


urlpatterns = [
	#first page : index page
	url(r'^$', IndexView.as_view(), name= 'index'),

	#profile_registration
	url(r'^profile_registration/$', ProfileCreateView.as_view(),
		name='profile_registration'),

	#dashboard
	url(r'^dashboard/$', DashboardView.as_view(), name= 'dashboard' ),

	# url(r'^/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'})

	url(r'^settings/$', SettingsView.as_view(), name='settings'),
]
