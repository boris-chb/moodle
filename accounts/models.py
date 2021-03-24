from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Instructor

    # Email will be treated as unique identifier instead of 'username'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    country = CountryField(blank_label='Where are you from?', default='IE')
    photo = models.ImageField(upload_to='profile_pic/%Y/%M/%d', blank=True)
    bio = models.CharField(max_length=200, default='')  # A short description

    def __str__(self):
        return f'Profile of {self.user.username}'
