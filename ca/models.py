from django.db import models
from allauth import app_settings as allauth_app_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import URLValidator
# from django.core.validators import MaxValueValidator
from TechnexUser.models import College,year_choices


class CAProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    year = models.IntegerField(choices=year_choices)
    mobile_number = models.BigIntegerField()
    whatsapp_number = models.BigIntegerField()
    college = models.ForeignKey(College,null = True)
    college_address = models.TextField()
    postal_address = models.TextField()
    pincode = models.PositiveIntegerField()
    profile_photo = models.TextField(validators=[URLValidator()],blank=True)

    def __unicode__(self):
        return '%s-%s' %(self.college, self.user)


class MassNotification(models.Model):
    ca = models.ManyToManyField(CAProfile)
    mass_message = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)
    mark_read = models.ManyToManyField(User, related_name='mark_read')

    def __unicode__(self):
        return self.mass_message
# bom = user.massnotification_set.all().order_by('-creation_time')
#request.user.massnotification_set.all()
#


class UserNotification(models.Model):
    ca = models.ForeignKey(CAProfile)
    message = models.TextField()
    mark_read = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.message

#request.user.usernotification_set.all()

#primary_key=True implies null=False and unique=True.
#Only one primary key is allowed on an object.
def get_user_image_folder(instance, filename):
    return "CAs/%s-%s-%s/%s" %(instance.user.first_name,instance.user.last_name,instance.user.caprofile.college, filename)
#You don't have to use request in Models, you use instance instead.

class Poster(models.Model):
    ca = models.ForeignKey(CAProfile)
    poster = models.ImageField(upload_to = get_user_image_folder)

    def __unicode__(self):
        return '%s' % self.poster

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

class Task(models.Model):
    taskId = models.AutoField(primary_key = True)
    taskName = models.CharField(max_length = 50)
    taskDescription = models.TextField()
    deadLine = models.DateTimeField()
    def __unicode__(self):
        return self.taskName

class TaskInstance(models.Model):
    task = models.ForeignKey(Task)
    ca = models.ForeignKey(CAProfile)
    status = models.SmallIntegerField(default = 0) #Added this field to show partial completion(0-10) of work
    def __unicode__(self):
        return u'%s'%self.status 