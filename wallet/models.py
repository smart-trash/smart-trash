from django.db import models
from accounts.models import User

# Create your models here.
class Wallet(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
     amount=models.FloatField(null=False,default=0)

