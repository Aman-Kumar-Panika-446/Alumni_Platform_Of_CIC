from django.contrib import admin
from opportunity.models import *

# Register your models here.

admin.site.register(Opportunity)
admin.site.register(Applicant)
admin.site.register(OpportunityReport)