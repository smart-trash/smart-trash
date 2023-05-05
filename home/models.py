from django.db import models

from accounts.models import User

# Create your models here.

class WasteAmount(models.Model):
     municipality = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
     amount=models.FloatField(null=False,default=100)

class RecyclerAmount(models.Model):
     recycler = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
     paper_amount=models.FloatField(null=False,default=100)
     metal_amount=models.FloatField(null=False,default=100)
     agent_amount=models.FloatField(null=False,default=100)

