from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import date,datetime
# Create your models here.

# TABLE FOR EVENT
class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="Event")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank= True)
    time = models.TimeField(null=True, blank= True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=100)
    posted_on = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='events/', blank= True, null= True)    
   
    # ADDING VALIDATION CHECKS
    def clean(self):
        today = datetime.today().date()

        if self.start_date and self.start_date < today:
            raise ValidationError({"start_date": "Start date can't be in past."})

        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date can't be before start date."})


    @property
    def event_status(self):
        if self.start_date > date.today():
            return "Upcoming"
        elif self.end_date:
            if self.end_date > date.today():
                return "Ongoing"
            else:
                return "Held"
        else:
            return "Held"

    def __str__(self): 
        return self.user.first_name + " - " + self.title
    
# TABLE FOR REPORTING AN EVENT
class EventReport(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="EventReport")
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    reported_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.reported_by} about {self.event.title} on {self.reported_on}"