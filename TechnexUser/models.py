from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ca.models import year_choices


def get_user_image_folder(instance, filename):
    return "technexuser/%s/%s" %(instance.user.caprofile.first_name, filename)

class UserStatus(models.Model):
    user = models.OneToOneField(User)
    is_ca = models.BooleanField(default=False)
    is_techuser = models.BooleanField(default=False)

    def __unicode__(self):
        return "ca : %s, techuser: %s" %(self.is_ca,self.is_techuser)


class TechProfile(models.Model):
    user = models.OneToOneField(User)
    year = models.IntegerField(choices=year_choices)
    mobile_number = models.BigIntegerField()
    college = models.CharField(max_length=250)
    profile_photo = models.ImageField(upload_to = get_user_image_folder,default=None)

    def __unicode__(self):
        return "%s %s-%s" %(self.user.first_name,self.user.last_name, self.college)
