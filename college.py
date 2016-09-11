import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ca_portal.settings")

import csv

from TechnexUser.models import College

with read('b.csv','rb') as f:
    data = csv.reader(f)
    for row in data:
        College.objects.create(collegeName=row[1])
