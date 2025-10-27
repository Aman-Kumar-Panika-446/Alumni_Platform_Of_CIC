from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from authentication.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.

def list_people(request):
    users = CustomUser.objects.all().exclude(Q(starting_year__isnull = True) | Q(enrolment_no__isnull = True)).order_by('first_name')

    search_query = request.GET.get("search")

    if search_query:
        users = users.filter(

            Q(first_name__icontains = search_query) |
            Q(last_name__icontains = search_query) |
            Q(course_name__icontains = search_query) |
            Q(ending_year__icontains = search_query) |
            Q(StudentDetails__home_town__icontains = search_query) |
            Q(AlumniDetails__location__icontains = search_query) |
            Q(AlumniDetails__WorkingProfessional__designation__icontains = search_query) |
            Q(AlumniDetails__WorkingProfessional__organization_name__icontains = search_query) |
            Q(AlumniDetails__Startup__startup_name__icontains = search_query) 

        )

    # APPLYING FILTERS
    role = request.GET.get("role")
    course = request.GET.get("course")
    location = request.GET.get("location")
    status = request.GET.get("status")
    designation = request.GET.get("designation")
    batch = request.GET.get("batch")

    if role:
        users = users.filter(role = role)
    
    if course:
        users = users.filter(course_name = course)
      
    if location:
        users = users.filter(
            Q(StudentDetails__home_town = location) |
            Q(AlumniDetails__location = location)
        )
    
    if status:
        users = users.filter(AlumniDetails__current_status = status)
        
    if designation:
        users = users.filter(AlumniDetails__WorkingProfessional__designation = designation)
      
    if batch:
        users = users.filter(ending_year = batch)
    
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ----- Clean GET params for pagination (exclude 'page') -----
    get_params = request.GET.copy()
    if 'page' in get_params:
        get_params.pop('page')
    query_string = get_params.urlencode()

    # PREPARING DATA TO DISPLAY
    locations = [] 
    alumni_location = AlumniDetails.objects.values_list('location', flat= True).distinct()
    student_location = StudentDetails.objects.values_list('home_town', flat=True).distinct()

    locations = alumni_location.union(student_location).order_by('location')
    
    designations = WorkingProfessional.objects.values_list('designation', flat= True).distinct().order_by('designation')
    batches = CustomUser.objects.all().exclude(ending_year__isnull = True).values_list('ending_year', flat=True).distinct().order_by('ending_year')

    context = {
        'users': page_obj,
        'locations': locations,
        'batches': batches,
        'designations':designations,
        'query_string': query_string

    }

    return render(request, "people/list_people.html", context)

def profile_details(request, user_id):
    user = get_object_or_404(CustomUser, pk = user_id)
    return render(request, "people/profile_details.html", {"user":user})


def upload_proofs(request):
    pass