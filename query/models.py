from django.db import models
from accounts.models import User
from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class Query(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
     content=models.TextField(max_length=150)
     created_date=models.DateTimeField(default=now)
