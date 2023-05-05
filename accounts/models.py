from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CUSTOMER = "CU"
    COLLECTION_AGENT = "CA"
    MUNICIPALITY = "MU"
    ADMIN = "AD"
    RECYCLER="RE"

    ROLES_CHOICES = [
        (CUSTOMER, "Customer"),
        (COLLECTION_AGENT, "Collection Agent"),
        (MUNICIPALITY, "Municipality"),
        (ADMIN, "Admin"),
        (RECYCLER, "Recycler"),
    ]

    phone = models.CharField(max_length=15)
    housename = models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    municipality = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True)
    postcode = models.CharField(max_length=6)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_image')
    role = models.CharField(
        max_length=2, choices=ROLES_CHOICES, null=False, default=ADMIN)


    @property
    def profile_image_url(self):
        try:
            url=self.profile_image.url
        except ValueError:
            url=""
        return url



class CollectionAgent(models.Model):
    aadhaar_number = models.CharField(max_length=12)
    license_number = models.CharField(max_length=16)
    aadhaar_image = models.ImageField(upload_to='aadhaar_image')
    license_image = models.ImageField(upload_to='license_image')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def aadhaar_image_url(self):
        try:
            url=self.aadhaar_image.url
        except ValueError:
            url=""
        return url

    @property
    def license_image_url(self):
        try:
            url=self.license_image.url
        except ValueError:
            url=""
        return url

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)