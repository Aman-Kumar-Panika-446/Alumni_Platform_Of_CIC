from django.shortcuts import render, redirect, get_object_or_404
from opportunity.models import *
from opportunity.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def list_opportunities(request):
    search_query = request.GET.get("search", '')
    filter_type = request.GET.get('filter', 'all')

    opps = Opportunity.objects.all().order_by('-posted_on')

    if search_query:
        opps = opps.filter(
            opportunity_type__icontains = search_query
        ) | opps.filter(
            organization_name__icontains = search_query
        ) | opps.filter(
            description__icontains = search_query
        ) | opps.filter(
            user__first_name__icontains = search_query
        )
    
    if filter_type == "posted_by_student":
        opps = opps.filter(user__role = "Student")
    elif filter_type == "posted_by_alumni":
        opps = opps.filter(user__role ="Alumni")
    elif filter_type == "posted_by_staff":
        opps = opps.filter(user__role ="Staff")
    
    context = {
        "opps": opps,
        "filter_type": filter_type,
        "search_query": search_query
    }
    return render(request, "opportunity/list_opportunity.html", context)

@login_required
def apply(request, pk):
    opp = get_object_or_404(Opportunity, pk = pk)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.opportunity = opp
            applicant.user = request.user
            applicant.save()
            messages.success(request, "Successfully applied for this opportunity")
            return redirect("opportunity:list_opportunities")
        else:
            messages.error(request, "Kindly fix the error.")
    else:
        form = ApplicantForm()
    
    return render(request, "opportunity/applicant.html", {"form":form})

@login_required
def post_opportunity(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST, request.FILES)
        if form.is_valid():
            opp = form.save(commit=False)
            opp.user = request.user
            opp.save()
            messages.success(request, "Opportunity has been posted.")
            return redirect("opportunity:list_opportunities")
        else:
            messages.error(request, "Kindly fix the errors")
    else:
        form = OpportunityForm()
    
    previous_url = request.META.get('HTTP_REFERER', 'opportunity:list_opportuniy')
    return render(request, "opportunity/opportunity_form.html", {"form":form, 'previous_url':previous_url})

def opportunity_details(request, opportunity_id):
    opp = get_object_or_404(Opportunity, pk = opportunity_id)
    previous_url = request.META.get('HTTP_REFERER', 'opportunity:list_opportuniy')
    return render(request, "opportunity/opportunity_details.html", {"opp": opp, "previous_url": previous_url})


@login_required
def edit_opportunity(request, opportunity_id):
    opp = get_object_or_404(Opportunity, pk = opportunity_id, user = request.user)

    if request.method == "POST":
        form = OpportunityForm(request.POST, request.FILES, instance=opp)
        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity details has been updated.")
            return redirect("opportunity:list_opportunities")
        else:
            messages.error(request, "Kindly input the details correctly.")
    else:
        form = OpportunityForm(instance=opp)
    
    previous_url = request.META.get('HTTP_REFERER', 'opportunity:list_opportunities')
    return render(request, "opportunity/opportunity_form.html", {"form": form, "opp":opp, "previous_url": previous_url})

@login_required
def delete_opportunity(request, opportunity_id):
    if request.method == 'POST':
        opp = get_object_or_404(Opportunity, pk = opportunity_id, user = request.user)
        opp.delete()
        messages.success(request, 'Opportunity has been deleted.')
        previous_url = request.META.get('HTTP_REFERER', 'opportunity:list_opportunities')
        return redirect(previous_url)

@login_required
def report_opportunity(request, opportunity_id):
    opp = get_object_or_404(Opportunity, pk = opportunity_id)
    if request.method == 'POST':
        form = OpportunityReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit = False)
            report.opportunity = opp
            report.reported_by = request.user
            report.save()
            messages.success(request, "Your report has been reported.")
            return redirect("opportunity:list_opportunities")
    else:
        form = OpportunityReportForm()

    return render(request, "opportunity/report_opportunity.html", {"form": form})

