from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.contrib import admin
from TechnexUser.views import *

app_name='technexuser'

urlpatterns = [

	url(r'^$', IndexView, name= 'index'),

	url(r'^login$', LoginView, name= 'login'),

	url(r'^register/$', RegisterView,name='register'),

	url(r'^dashboard/$', DashboardView,name='dashboard'),

	url(r'^logout/$', LogoutView, name='logout')

]
