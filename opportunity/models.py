from django.db import models
from authentication.models import CustomUser

# # Create your models here.

# TABLE FOR EVENT
class Opportunity(models.Model):
    opportunity_choices = (
        ('Internship', 'Internship'),
        ('Job', 'Job')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="Opportunity")
    opportunity_type = models.CharField(max_length=15, choices= opportunity_choices)
    organization_name = models.CharField(max_length=200, null= True, blank= True)
    role = models.CharField(max_length=100)
    duration = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    last_date = models.DateField()
    posted_on = models.DateField(auto_now=True)
    image = models.ImageField(default="opportunity/default.jpg", upload_to='opportunity', blank= True, null= True)
    

    def __str__(self): 
        return self.user.first_name + " - " + self.opportunity_type
    
# TABLE FOR APPLICANTS
class Applicant(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name= 'Applicants')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="CustomUser")
    cv = models.FileField(upload_to="applicant's_cv")
    remark = models.TextField(blank=True, null=True, max_length=200)

    def __str__(self):
        return f"{self.opportunity.user.first_name} applied for {self.opportunity.role} @{self.opportunity.organization_name}"

# TABLE FOR REPORTING AN OPPORTUNITY
class OpportunityReport(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="OpportunityReport")
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    reported_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.reported_by} about {self.opportunity.opportunity_type} on {self.reported_on}"