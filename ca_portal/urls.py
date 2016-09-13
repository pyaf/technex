from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^ca/',include('ca.urls')),
    url(r'^',include('TechnexUser.urls')),
    url(r'^task/',include('task.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('allauth.urls')),


]
