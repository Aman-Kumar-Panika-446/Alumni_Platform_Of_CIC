from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Built in AbstractUser
'''
username      # unique identifier (150 chars by default)
first_name    # optional, 150 chars
last_name     # optional, 150 chars
email         # optional, EmailField
password      # hashed password
is_staff      # can log into admin site
is_active     # whether account is active
is_superuser  # has all permissions
last_login    # last login datetime
date_joined   # when the user was created

'''

# Table containing Common attribute
class CustomUser(AbstractUser):
    role_choices = [
        ('Student', 'Student'),
        ('Alumni', 'Alumni')
    ]

    course_choices = [
        ("BTECH","BTECH"),
        ("BA HONOURS", "BA HONOURS")
    ]

    role = models.CharField(max_length=15, null=True, choices=role_choices) # STUDENT OR ALUMNI OR STAFF
    roll_no = models.CharField(unique=True, null= True) 
    enrolment_no = models.CharField(unique=True, null= True)
    starting_year = models.IntegerField(null = True)
    ending_year = models.IntegerField(null = True)
    course_name = models.CharField(max_length=50, null= True, choices=course_choices) 
    profile_pic = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/default1.png", 
        blank=True,
        null=True
    )

    def __str__(self):
        return self.first_name + " " + self.last_name

# Student Details
class StudentDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='StudentDetails')
    current_year = models.IntegerField()
    home_town = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name + " " +self.user.last_name +" - "+ str(self.current_year) + " Year"

# Basic Details of Alumni
class AlumniDetails(models.Model):

    status_choices = [
        ("Job", "Job"),
        ("Higher Studies", "Higher Studies"),
        ("Startup", "Startup"),
        ("Other", "Other")
    ]

    alumni = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="AlumniDetails")
    current_status = models.CharField(max_length=20, choices=status_choices) # WORKING PROF OR HIGHER STUDIES OR "OTHER" 
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.alumni.first_name +" - "+ self.current_status


# FOR WORKING PROFESSIONALS
class WorkingProfessional(models.Model):
    alumni = models.OneToOneField(AlumniDetails, on_delete=models.CASCADE, related_name="WorkingProfessional")
    organization_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.alumni.alumni.first_name + " - "+ self.organization_name

# FOR HIGHER STUDIES
class HigherStudies(models.Model):
    alumni = models.OneToOneField(AlumniDetails, on_delete=models.CASCADE, related_name="HigherStudies")
    organization_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)

    def __str__(self):
        return self.alumni.alumni.first_name + " - " +  self.alumni.current_status


# FOR STARTUP
class Startup(models.Model):
    alumni = models.OneToOneField(AlumniDetails, on_delete=models.CASCADE, related_name="Startup")
    startup_name = models.CharField(max_length= 30, null= False, blank= False)
    description = models.CharField(max_length=200, blank= True, null= True)

    def __str__(self):
        return self.alumni.alumni.first_name + " " + self.alumni.alumni.last_name + " - " + self.startup_name

# FOR OTHER
class Others(models.Model):
    alumni = models.OneToOneField(AlumniDetails, on_delete=models.CASCADE, related_name="Others")
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.alumni.alumni.first_name + " " + self.alumni.alumni.last_name

# FOR MANUAL VERIFICATION
class ManualVerification(models.Model):
    username = models.CharField(max_length=30, blank=False, null=False)
    email_id = models.EmailField(blank=False, null=False)
    
    id_type = models.CharField(max_length=30, blank=False, null=False)
    id_file = models.FileField(upload_to = "id_proofs")

    clg_id_type= models.CharField(max_length=30, blank=False, null=False)
    clg_id_file = models.FileField(upload_to = "id_proofs")

    def __str__(self):
        return self.username
