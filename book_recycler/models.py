import re
from django.db import models
from accounts.models import User
from django.utils.timezone import now

# Create your models here.
class RecyclerBooking(models.Model):

    PENDING = "Pending"
    ASSIGNED = "Assigned"
    COLLECTED = "Collected"
    VERIFIED ="Verified"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ASSIGNED, "Assigned "),
        (COLLECTED, "Collected"),
        (VERIFIED, "Verified"),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='related_user')
    recycler = models.ForeignKey(User, on_delete=models.CASCADE,related_name='related_recycler')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, default=PENDING)
    paper_waste=models.IntegerField()
    metal_waste=models.IntegerField()
    created_date=models.DateTimeField(default=now)
    collection_date=models.DateField(null=True)
    collection_agent=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    