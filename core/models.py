from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.



# ORM
# Profile table / class /relation
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # if user will delete profile will also delete usint models.cascade
    age = models.PositiveIntegerField(null=True) # null means it not required to have value while creating the object
    gender = models.CharField(max_length=6, null=True)
    city = models.CharField(max_length=40, null=True)
    country = models.CharField(max_length=40, null=True)


    def __str__(self):
        return f"user profile {self.user.username}"

# create user using python3 manage.py createsuperuser

# post save signal (whenever user will create one profile of that user will also create)
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, **kwargs):
    try:
        Profile.objects.create(user=instance)
        print("profile is created...")
    except Exception as e:
        print(e)
        pass



class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    sales_number = models.PositiveIntegerField()
    revenue = models.FloatField()
    date = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.username} product -{self.product} \
                  revenue - {self.revenue}"






