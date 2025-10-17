# Create your views here.
from django.shortcuts import render, redirect
from datetime import datetime
from .utils.qr_utils import read_qr_from_image, split_qr_data
import random, re, string
from .utils.send_email import send_otp_to_mail
from django.contrib import messages
from .models import * 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def login_view(request):
    if request.method == "POST":
        email_id = request.POST.get("email_id")
        password = request.POST.get("password")

        try:
            user_data = CustomUser.objects.get(email = email_id)
            user = authenticate(username = user_data.username, password = password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.first_name}")
            return redirect("index")
        else:
            messages.error(request, "Invalid Email Id or Password")
            return redirect("login_view")
        
    return render(request, 'authentication/login.html')


def forgot_password(request):
    return render(request, "authentication/forgot_password.html")

def fetch_email(request):

    if request.method == 'POST':
        action = request.POST.get("action")
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email = email)
        except CustomUser.DoesNotExist:
            user = None

        if user is None:
            messages.error(request, "No user is registered with this email id.")
            return redirect("forgot_password")
        
        if action == "send_otp":
            otp = str(random.randint(100000, 999999))
            request.session["email"] = email
            request.session["otp"] = otp  

            success = send_otp_to_mail(email, otp)
            if not success:
                messages.error(request, "Failed to send OTP. Try again.")
                return redirect("forgot_password")

            request.session['otp_sent'] = True
            messages.success(request, "OTP sent successfully!")
            return render(request, "authentication/forgot_password.html")

        elif action == "verify_otp":
            otp = request.POST.get("otp")
            if otp == str(request.session.get("otp")):
                messages.success(request, "OTP verified successfully!")
                return render(request, "authentication/reset_password.html", {"user":user})
            else:
                messages.error(request, "Invalid OTP. Try again.")
                return redirect("forgot_password")

        elif action == "resend_otp":
            email = request.session.get("email")
            otp = str(random.randint(100000, 999999))
            request.session["otp"] = otp

            success = send_otp_to_mail(email, otp)
            if not success:
                messages.error(request, "Failed to resend OTP.")
                return redirect("forgot_password")

            request.session['otp_sent'] = True
            messages.success(request, "OTP resent successfully!")
            return redirect("forgot_password")
        

    return redirect("login_view")

def reset_password(request):
    if request.method == "POST":
        email_id = request.session["email"]
        user = CustomUser.objects.get(email = email_id)
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request, "Your password has been reset. Kindly login with new credentials")
            return redirect("login_view")
        else:
            messages.error(request, "Your password is not matching")
            return render(request, "authentication/reset_password.html")
        
    return redirect("login_view")



def email_verification(request):
    if request.method == "POST":
        action = request.POST.get("action")
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email = email)
        except CustomUser.DoesNotExist:
            user = None
        
        if user is not None:
            messages.error(request, "User is already registered with this email id")
            return redirect("email_verification")
        
        if action == "send_otp":
            otp = str(random.randint(100000, 999999))
            request.session["email"] = email
            request.session["otp"] = otp  

            success = send_otp_to_mail(email, otp)
            if not success:
                messages.error(request, "Failed to send OTP. Try again.")
                return redirect("email_verification")

            request.session['otp_sent'] = True
            messages.success(request, "OTP sent successfully!")

        elif action == "verify_otp":
            otp = request.POST.get("otp")
            if otp == str(request.session.get("otp")):
                request.session["otp_verified"] = True
                messages.success(request, "OTP verified successfully!")
                return redirect("upload_document")
            else:
                messages.error(request, "Invalid OTP. Try again.")

        elif action == "resend_otp":
            email = request.session.get("email")
            if not email or not email.endswith("@cic.du.ac.in"):
                messages.error(request, "Invalid Email Id.")
                return redirect("email_verification")

            otp = str(random.randint(100000, 999999))
            request.session["otp"] = otp

            success = send_otp_to_mail(email, otp)
            if not success:
                messages.error(request, "Failed to resend OTP.")
                return redirect("email_verification")

            request.session['otp_sent'] = True
            messages.success(request, "OTP resent successfully!")
            return redirect("email_verification")  

    
    return render(request, "authentication/email_verification.html")

def upload_document(request):
    if request.session.get("otp_verified"):
        return render(request, "authentication/upload_document.html")
    
    return redirect("email_verification")


def user_details(request):
        if request.method == "POST":
            file = request.FILES["document"]
            with open("temp.png", "wb") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            qr_text = read_qr_from_image("temp.png")
            
            #CHECKING WHETHER WE GET DATA OR NOT
            if qr_text is None:
                messages.error(request, "Sorry, Unable to find details")
                return redirect("upload_document")
            
            name, roll_no, enrollment,starting_year, ending_year, role = split_qr_data(qr_text)
            
            # Checking whether the user is CICian or Not
            required_formats = ["CINCBTIM", "CINCBHSS"]
            format = re.sub('[^A-Z]','',enrollment)

            if format not in required_formats:
                messages.error(request, "You are not CICian")
                return render(request,"authentication/upload_document.html")
            
            course_name = "BTECH" if format == "CINCBTIM" else "BA HONOURS"
            emailId = request.session.get("email")
            details = {
                "emailId": emailId,
                "name": name,
                "roll_no": roll_no,
                "enrollment_no": enrollment,
                "batch_year":f"{starting_year} - {ending_year}",
                "role": role,
                "course_name":course_name
            }

            request.session['academic_details'] = details
            return render(request, "authentication/user_details.html", {"details": details})

        return redirect("email_verification") 


def signup_data(request):
    if request.method == "POST":
        details = request.session.get("academic_details")
        return render(request, "authentication/signup_data.html", {"details": details})
    
    return redirect("email_verification")



def save_signup(request):
    if request.method == "POST":

        # SECURITY CHECK
        academic_details = request.session.get("academic_details")
        first_name = str(request.POST.get("first_name")).strip().lower()
        last_name = str(request.POST.get("last_name")).strip().lower()
        last_name = re.sub("[^a-z]",'',last_name)
        full_name = str(academic_details['name']).lower()

        # VERIFYING THE USER'S NAME
        if(first_name+last_name != full_name):
            messages.error(request,"Your first & last name should match with extracted data")
            return render(request, "authentication/signup_data.html", {"details":academic_details})
        
        # CHECKING FOR USERNAME
        username= request.POST.get("username")
        user_data = CustomUser.objects.filter(username = username).exists()
        if user_data:
            messages.error(request, "Try some another unique username.")
            return render(request, "authentication/signup_data.html", {"details":academic_details})

        role = academic_details['role']
        batch_year = academic_details["batch_year"]
        start, end = batch_year.split("-")

        user = CustomUser.objects.create_user(
                # BUILT IN ATTRIBUTES
                first_name = first_name,
                last_name = last_name,
                email=request.session.get("email"),
                password=request.POST.get("password"),
                username= request.POST.get("username"),

                # CUSTOM ATTRIBUTES
                role = role,
                roll_no= academic_details["roll_no"],
                enrolment_no=academic_details["enrollment_no"],
                starting_year=int(start),
                ending_year= int(end),
                course_name = academic_details["course_name"]
            )

        if role == "Alumni":

            status_choices = {
                "job": "Job",
                "higher_studies": "Higher Studies",
                "startup": "Startup",
                "other": "Other"
            }

            career_path = request.POST.get("career_path")
            alumni = AlumniDetails.objects.create(
                user = user,
                current_status = status_choices[career_path],
                location = request.POST.get("location")
            )

            if career_path == "job":
                WorkingProfessional.objects.create(
                    alumni = alumni,
                    organization_name=request.POST.get("job_organization"),
                    designation=request.POST.get("job_designation")
                )
            elif career_path == "higher_studies":
                HigherStudies.objects.create(
                    alumni = alumni,
                    organization_name=request.POST.get("higher_organization"),
                    domain = request.POST.get("higher_domain")
                )
            elif career_path == "startup":
                Startup.objects.create(
                    alumni = alumni,
                    startup_name=request.POST.get("startup_name"),
                    description = request.POST.get("startup_description")
                )
            else:
                Others.objects.create(
                    alumni = alumni,
                    description = request.POST.get("other_description")                )
        else:
            current_year = datetime.now().year
            current_month = datetime.now().month

            year_of_student = current_year - int(start)

            if(current_month >= 8):
                year_of_student += 1

            StudentDetails.objects.create(
                user = user,
                current_year = year_of_student,
                home_town = request.POST.get("home_town")
            )
        messages.success(request, "Your account has been created.")
        login(request, user)
        return redirect("home_page")

    return redirect('email_verification') 

def manual_verification(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        email_id = request.POST.get("email")
        id_type = request.POST.get("id_proof_option")
        id_file = request.FILES.get("id_proof_file")
        clg_id_type = request.POST.get("college_proof_option")
        clg_id_file = request.FILES.get("clg_proof_file")

        # CREATE USER
        ManualVerification.objects.create(
            username = username,
            email_id = email_id,
            id_type = id_type,
            id_file = id_file,
            clg_id_type = clg_id_type,
            clg_id_file = clg_id_file
        )

        messages.success(request, "Thanks For submitting the documents. Our Team will contact you very soon...")
        return redirect("index")
        
    return render(request, "authentication/manual_verification.html")


@login_required(login_url='login_view')
def home(request):
    return render(request, "authentication/home.html")


