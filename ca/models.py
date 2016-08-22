from django.db import models
from allauth import app_settings as allauth_app_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.validators import MaxValueValidator

year_choices = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5,'Fifth'),
    ]
class UserProfile(models.Model):

    # allauth_app_settings.USER_MODEL = auth.User
    user = models.OneToOneField(User, primary_key=True)

    name = models.CharField(max_length=100)
    year = models.IntegerField(choices=year_choices)
    mobile_number = models.BigIntegerField()
    whatsapp_number = models.BigIntegerField()
    college = models.CharField(max_length=250)
    college_address = models.TextField()
    postal_address = models.TextField()
    pincode = models.PositiveIntegerField()
    profile_completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
'''use BigIntegerField for postgresql'''
'''for sqlite3 etc. use IntegerField(validators=[MaxValueValidator(9999999999)])'''
# @receiver(post_save, sender=User)
# def create_profile(sender,created, instance, **kwargs):
#     if created:
#         user_profile = UserProfile(user = instance)
#         user_profile.save()

    # #where to redirect after successful userprofile registration
    # def get_absolute_url(self):
    #     return reverse('dashboard',kwargs={'pk':self.pk})
    # or
    # def get_absolute_url(self):
    #     return u'/some_url/%d' % self.id

class MassNotification(models.Model):
    user = models.ManyToManyField(User)
    mass_message = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)
    mark_read = models.ManyToManyField(User, related_name='mark_read')

    def __unicode__(self):
        return self.mass_message
# bom = user.massnotification_set.all().order_by('-creation_time')
#request.user.massnotification_set.all()
#


class UserNotification(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()
    mark_read = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.message
#request.user.usernotification_set.all()

#primary_key=True implies null=False and unique=True.
#Only one primary key is allowed on an object.
def get_user_image_folder(instance, filename):
    return "%s/%s" %(instance.user.userprofile.name, filename)
#You don't have to use request in Models, you use instance instead.

class Poster(models.Model):
    user = models.ForeignKey(User)
    poster = models.ImageField(upload_to = get_user_image_folder)

    def __unicode__(self):
        return '%s' % self.poster


class TechnexUser(models.Model):
    name = models.CharField(max_length=100)
    college = models.CharField(max_length = 250)
    year = models.IntegerField(choices=year_choices)
    mobile_number = models.IntegerField()
    whatsapp_number = models.IntegerField()

    def __unicode__(self):
        return '%s-%s' %(self.name, self.college)
