from django.db import models
from accounts.models import User

# Create your models here.


class SmartBin(models.Model):
    bin_id = models.CharField(max_length=36,null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    fill_status=models.BooleanField(null=True)
