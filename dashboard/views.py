from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.urls import *
from authentication.models import *
from datetime import datetime
from .forms import ExperienceForm, SkillForm
from events.models import Event

# Create your views here.

# RENDERING DASHBOARD
@login_required(login_url="login_view")
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

# UPDATING PROFILE IMAGES
@login_required
def update_profile_pic(request):
    
    user_data = request.user

    if request.method == 'POST':
        profile_pic = request.FILES.get("profile_pic")
        user_data.profile_pic = profile_pic
        user_data.save()
    messages.success(request, "Profile Images has been updated.")
    return redirect("dashboard:dashboard")


# EDITING THE CURRENT STATUS
@login_required
def edit_current_status(request):
    
    # SAVING THE DATA
    if request.method == "POST":

        user_data = request.user
        
        # WHETHER THE USER IS STUDENT OR ALUMNI ?
        
        if user_data.role == "Alumni":
            alumni_data = AlumniDetails.objects.get(user = request.user)
            new_role = request.POST.get("career_path")
            new_location = request.POST.get("location")

            status_choices = {
                "job": "Job",
                "higher_studies": "Higher Studies",
                "startup": "Startup",
                "other": "Other"
            }

            # UPDATING THE AlumniDetails TABLE
            alumni_data.current_status = status_choices[new_role]
            alumni_data.location = new_location
            alumni_data.save()

            # DELETING THE CORRESPONDING TABLE
            WorkingProfessional.objects.filter(alumni = alumni_data.pk).delete()
            HigherStudies.objects.filter(alumni = alumni_data.pk).delete()
            Startup.objects.filter(alumni = alumni_data.pk).delete()
            Others.objects.filter(alumni = alumni_data.pk).delete()

            # CREATING A NEW TABLE WITH RESPECT TO NEW ROLE
            if new_role == "job":
                WorkingProfessional.objects.create(
                    alumni = alumni_data,
                    organization_name=request.POST.get("job_organization"),
                    designation=request.POST.get("job_designation")
                )
            elif new_role == "higher_studies":
                HigherStudies.objects.create(
                    alumni = alumni_data,
                    organization_name=request.POST.get("higher_organization"),
                    domain = request.POST.get("higher_domain")
                )
            elif new_role == "startup":
                Startup.objects.create(
                    alumni = alumni_data,
                    startup_name=request.POST.get("startup_name"),
                    description = request.POST.get("startup_description")
                )
            else:
                Others.objects.create(
                    alumni = alumni_data,
                    description = request.POST.get("other_description")
                )

            messages.success(request, "Your current status has been updated.")
            return redirect("dashboard:dashboard")

        # IF THE USER IS STUDENT
        else:
            student_data = StudentDetails.objects.get(user = user_data)
            student_data.home_town = request.POST.get("home_town")
            student_data.bio = request.POST.get("bio")
            student_data.save()

            messages.success(request, "Your Details has been updated.")
            return redirect("dashboard:dashboard")
    
    # SHOWING THE FORM
    else:
        return render(request, "dashboard/career_path.html", {"user_data": request.user})




# LOGOUT FEATURE
@login_required()
def user_logout(request):
    logout(request)
    messages.info(request,"You have been logged out successfuly...")
    return redirect("index")


# NOW DEALING WITH EXPERIENCE TAB
@login_required()
def view_experience(request):
    experience = Experience.objects.filter(user = request.user)
    return render(request, "dashboard/experience.html", {"experience": experience})


@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, "Your Experience has been added successfully.")
            return redirect("dashboard:view_experience")
        else:
            messages.error(request, "Kindly fix the error")
    else:
        form = ExperienceForm()
    
    return render(request, "dashboard/experience_form.html", {"form":form, "title":"Add Experience"})
    

@login_required
def edit_experience(request, pk):
    experience = get_object_or_404(Experience, pk = pk, user = request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES, instance= experience)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Experience has been updated.")
            return redirect("dashboard:view_experience")
        else:
            messages.error(request, "Kindly fix the error.")
    else:
        form = ExperienceForm(instance=experience)

    return render(request, "dashboard/experience_form.html", {"form":form, "title": "Edit Your Experience"})


@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk = pk, user = request.user)
    if request.method == 'POST':
        experience.delete()
        messages.success(request, "Your Experience has been deleted.")
        return redirect("dashboard:view_experience")


# NOW DEALING WITH SKILLS
@login_required
def view_skills(request):
    all_skills = Skill.objects.filter(user = request.user)
    return render(request, "dashboard/skills.html", {"all_skills":all_skills})


@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, "Your skill has been added.")
            return redirect("dashboard:view_skills")
        
        else:
            messages.error(request, "Kindly fix the error")

    else:
        form = SkillForm()
    
    return render(request, "dashboard/skill_form.html", {"form": form, "title": "Add Experience"})


@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, user = request.user, pk = pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES, instance= skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Skill has been edited.")
            return redirect("dashboard:view_skills")
        else:
            messages.error(request, "Kindly fix the error.")
    else:
        form = SkillForm(instance=skill)

    return render(request, "dashboard/skill_form.html", {"form":form, "title": "Edit Skill"})


@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk = pk, user = request.user)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Your Skill has been deleted.")
        return redirect("dashboard:view_skills")


# HANDLING EVENT SECTION
@login_required
def view_events(request):
    events = Event.objects.filter(user = request.user)
    return render(request, "dashboard/events.html", {"events":events})