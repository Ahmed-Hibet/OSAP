from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

'''
class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(
        self, email, password, roll, username=None, first_name=None, 
        last_name=None, is_staff=False, is_active=True, gender=None, 
        national_id=None, birth_date=None, region='None', city=None, 
        phone_number=None, is_verified=False, education_level=None, occupation=None):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        if not roll:
            raise ValueError('User must have a roll')
        
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.roll = roll
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_active = is_active
        user.gender = gender
        user.national_id = national_id
        user.birth_date = birth_date
        user.region = region
        user.city = city
        user.phone_number = phone_number
        user.is_verified = is_verified
        user.education_level = education_level
        user.occupation = occupation
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, roll, username=None, **kwargs):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        if not roll:
            raise ValueError('User must have a roll')
        
        user = self.model(
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.roll = roll
        user.username = username
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user
'''

class Occupation(models.Model):
    work_type = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.work_type    


class EducationLevel(models.Model):
    level_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.level_name


class Roll(models.Model):
    roll_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.roll_name


class User(AbstractUser):
    GENDER = [('M', 'Male'), ('F', 'Female')]
    REGIONS = [
        ('None', 'None'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Afar', 'Afar'),
        ('Oromia', 'Oromia'),
        ('Amhara', 'Amhara'),
        ('Tigray', 'Tigray'),
        ('Somali', 'Somali'),
        ('Sidama', 'Sidama'),
        ('Harari', 'Harari'),
        ('Gambela', 'Gambela'),
        ('Benishangul-Gumuz', 'Benishangul-Gumuz'),
        ('Dire Dawa', 'Dire Dawa'),
        ('SWEP', 'South West Ethiopia Peoples'),
        ('SNNP', 'Southern Nations, Nationalities, and Peoples'),
    ]
    email = models.EmailField(max_length=254, verbose_name='email address', unique=True)
    gender = models.CharField(choices=GENDER, max_length=1, blank=True, null=True)
    # username = models.CharField(blank=True, null=True, max_length=50)
    national_id = models.CharField(blank=True, null=True, max_length=50)
    birth_date = models.DateField(blank=True, null=True)
    region = models.CharField(choices=REGIONS, default='None', max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, blank=True, null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    roll = models.ForeignKey(Roll, on_delete=models.PROTECT, blank=True, null=True)
    is_verified = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'