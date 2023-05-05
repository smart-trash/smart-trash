from django.db import models

# Create your models here.
class ForgotPassword(models.Model):
    id=models.CharField(max_length=36,null=False,primary_key=True)
    email=models.CharField(max_length=100,null=False)