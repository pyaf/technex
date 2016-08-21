from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin.options import ModelAdmin
from ca.models import *

#Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

#Define a new User Admin
class UserAdmin(UserAdmin):

    def name(obj):
        return "%s" % obj.userprofile.name
    def college(obj):
        return "%s" % obj.userprofile.college
    def mobile_number(obj):
        return "%s" % obj.userprofile.mobile_number

    name.short_description = 'Name'
    college.short_description = 'College'
    mobile_number.short_description = 'Mobile No.'

    inlines = (UserProfileInline, )
    list_display = (name, college, mobile_number, 'email', 'is_staff')

class MassNotificationAdmin(admin.ModelAdmin):
    list_display = ['mass_message']

class UserNotificationAdmin(admin.ModelAdmin):
    def name(obj):
        return "%s" % obj.user.userprofile.name
    name.short_description = 'Name'
    list_display = [name,'message','mark_read']

class PosterAdmin(admin.ModelAdmin):
    def name(obj):
        return "%s" % obj.user.userprofile.name
    name.short_description = 'Name'
    list_display = (name,'poster')

class TechnexUserAdmin(admin.ModelAdmin):
    list_display = ('name','college')


#Re-register UserAdmin
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Poster, PosterAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(MassNotification, MassNotificationAdmin)
admin.site.register(UserNotification, UserNotificationAdmin)
admin.site.register(TechnexUser,TechnexUserAdmin)
