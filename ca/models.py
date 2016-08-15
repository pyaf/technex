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

    name = models.CharField(max_length=50)
    year = models.IntegerField(choices=year_choices)
    mobile_number = models.PositiveIntegerField()
    whatsapp_number = models.PositiveIntegerField()
    college = models.CharField(max_length=100)
    college_address = models.TextField(max_length=250)
    postal_address = models.TextField()
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return self.name +'-'+ self.college +'-' +self.user.email

    def __unicode__(self):
        return self.name +'-'+ self.college +'-'+self.user.email

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
