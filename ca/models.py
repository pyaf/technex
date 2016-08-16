from django.db import models
from allauth import app_settings as allauth_app_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    year_choices = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5,'Fifth'),
    ]
    # allauth_app_settings.USER_MODEL = auth.User
    user = models.OneToOneField(User,
                                primary_key=True,)

    name = models.CharField(max_length=100)
    year = models.IntegerField(choices=year_choices)
    mobile_number = models.PositiveIntegerField()
    whatsapp_number = models.PositiveIntegerField()
    college = models.CharField(max_length=250)
    college_address = models.TextField()
    postal_address = models.TextField()
    pincode = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

'''
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
'''
    # #where to redirect after successful userprofile registration
    # def get_absolute_url(self):
    #     return reverse('dashboard',kwargs={'pk':self.pk})
    # or
    # def get_absolute_url(self):
    #     return u'/some_url/%d' % self.id

class MassNotification(models.Model):
    user = models.ManyToManyField(User)
    mass_message = models.TextField()

    def __unicode__(self):
        return self.mass_message


class UserNotification(models.Model):
    user = models.ForeignKey(User)
    message = models.TextField()

    def __unicode__(self):
        return self.message

#primary_key=True implies null=False and unique=True.
#Only one primary key is allowed on an object.

class Poster(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    poster_1 = models.ImageField(upload_to='posters')
    poster_2 = models.ImageField(upload_to='posters')
    poster_3 = models.ImageField(upload_to='posters')
    poster_4 = models.ImageField(upload_to='posters')

    # def __unicode__(self):
    #     return "%s's posters " % self.user.userprofile.name
    def __unicode__(self):
        return '%s' % self.poster_1
