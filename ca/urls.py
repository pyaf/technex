from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.contrib import admin
from ca.views import (IndexView,ProfileCreateView,
					DashboardView,AccountDetailView,
					NotificationsView,ToDoListView, PosterUploadView)


urlpatterns = [
	#first page : index page
	url(r'^$', IndexView.as_view(), name= 'index'),

	#profile_registration
	url(r'^profile_registration/$', ProfileCreateView.as_view(),
		name='profile_registration'),

	#dashboard
	url(r'^dashboard/$', DashboardView.as_view(), name= 'dashboard' ),

	# url(r'^/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'})

	url(r'^settings/$', AccountDetailView, name='settings'),

	#notification
	url(r'^notifications/$', NotificationsView, name='notifications'),

	#to_do_list
	url(r'^to_do_list/$', ToDoListView.as_view(), name='to_do_list'),

	#poster_upload
	url(r'^poster_upload/$', PosterUploadView, name='poster_upload'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
