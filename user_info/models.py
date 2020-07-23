from django.db import models

from django.contrib.auth.models import User

# Model for user information
class UserProfileInfo(models.Model):

    # creating user object by using default user object
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    date_of_birth = models.DateField()

    phone = models.CharField(max_length=10)

    passport_num = models.CharField(max_length = 9)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
