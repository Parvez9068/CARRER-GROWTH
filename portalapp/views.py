from django.shortcuts import render, redirect, HttpResponse
from .models import Job,JobApplication,Feedback,SavedJob
from .forms import RegisterJob
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

# Create your views here.

from django.contrib.auth.decorators import login_required


def dashboard(req):
    alljob = Job.objects.all()
    context = {"alljob": alljob}
    return render(req, "dashboard.html", context)


@login_required
def index(req):
    user = req.user
    alljob = Job.objects.filter(user=user)
    context = {"alljob": alljob}
    return render(req, "index.html", context)

@login_required
def registerjob(request):
    if request.method == "POST":
        form = RegisterJob(request.POST, request.FILES)
        if form.is_valid():
            job_instance = form.save(commit=False)
            job_instance.user = request.user  # Assuming there's a ForeignKey to User in your Job model
            job_instance.save()
            # messages.success(request, 'Job registered successfully!')  # Add success message
            return redirect("/index")
    else:
        form = RegisterJob()
    return render(request, "registerjob.html", {"form": form})
@login_required
def removejob(req, jobid):
    user = req.user
    job = get_object_or_404(Job, pk=jobid, user=user)
    job.delete()
    return redirect("/index")


def updatejob(req, jobid):
    user = req.user
    job = get_object_or_404(Job, pk=jobid, user=user)
    if req.method == "POST":
        form = RegisterJob(req.POST, req.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect("/index")
    else:
        form = RegisterJob(instance=job)
    context = {"form": form, "job": job}
    return render(req, "updatejob.html", context)

from django.core.exceptions import ValidationError


def validate_password(password):
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # Check maximum length
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters.")

    # Initialize flags for character checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    # Check for character variety
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not has_digit:
        raise ValidationError("Password must contain at least one digit.")
    if not has_special:
        raise ValidationError(
            "Password must contain at least one special character (e.g., @$!%*?&)."
        )

    # Check against common passwords
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "abc123",
    ]  # Add more common passwords
    if password in common_passwords:
        raise ValidationError("This password is too common. Please choose another one.")

#FOR SIGNUP 
def signup(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        email = req.POST["email"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "signup.html", context)

        if uname == "" or email == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)
        elif uname.isdigit():
            context["errmsg"] = "Username cannot consist solely of numbers."
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(
                    username=uname, email=email, password=upass
                )
                userdata.set_password(upass)
                userdata.save()
                return redirect("/signin")
            except:
                context["errmsg"] = "User Already exists"
                return render(req, "signup.html", context)
    else:
        context = {}
        context["errmsg"] = ""
        return render(req, "signup.html", context)



#FOR SIGNIN
def signin(req):
    if req.method == "POST":
        email = req.POST["email"]
        upass = req.POST["upass"]
        context = {}
        if email == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signin.html", context)
        else:
            try:
                user = User.objects.get(email=email)  # Retrieve user by email
                userdata = authenticate(username=user.username, password=upass)
                print(userdata)
                if userdata is not None:
                    login(req, userdata)
                    return redirect("/")
                else:
                    context["errmsg"] = "Invalid username and password"
                    return render(req, "signin.html", context)
            except:
                context["errmsg"] = "User doesn't exist"
                return render(req, "signin.html", context)
    else:
        return render(req, "signin.html")


def userlogout(req):
    logout(req)
    return redirect("/")


from django.contrib import messages

#FOR RESET PASSWORD REQUEST
def request_password_reset(req):
    if req.method == "POST":
        email = req.POST.get("email")
        context = {}

        # Check if the email exists
        try:
            user = User.objects.get(email=email)
            # Redirect to the password reset page
            return redirect("reset_password", username=user.username)
        except User.DoesNotExist:
            context["errmsg"] = "No account found with that email."
            return render(req, "request_password_reset.html", context)

    return render(req, "request_password_reset.html")

# FOR RESET PASSOWRD
def reset_password(req, username):
    try:
        # Get the user by username
        user = User.objects.get(username=username)

        # Process POST request to reset password
        if req.method == "POST":
            new_password = req.POST.get("new_password")
            
            try:
                # Validate the new password
                validate_password(new_password)
                # Set and hash the new password
                user.set_password(new_password)
                user.save()

                # Display success message and redirect to signin
                messages.success(req, "Your password has been reset successfully.")
                return redirect("signin")

            except ValidationError as e:
                # Handle validation errors and stay on the reset password page
                messages.error(req, str(e))
                return render(req, "reset_password.html", {"username": username})

        # Render the reset password page
        return render(req, "reset_password.html", {"username": username})

    except User.DoesNotExist:
        # Handle case where user does not exist
        messages.error(req, "User not found.")
        return redirect("request_password_reset")

from django.db.models import Q

# FOR JOB SEARCH
def searchjob(req):
    query = req.GET.get("q")
    errmsg = ""

    if req.user.is_authenticated:
        if query:
            alljob = Job.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)  | Q(salary__icontains=query)| Q(location__icontains=query)
            )
            if len(alljob) == 0:
                errmsg = "No result found"
        else:
            alljob = Job.objects.all()

        context = {"alljob": alljob, "query": query, "errmsg": errmsg}
        return render(req, "dashboard.html", context)
    else:
        if query:
            alljob = Job.objects.filter(
                Q(title__icontains=query) | Q(company__icontains=query)  | Q(salary__icontains=query)| Q(location__icontains=query)
            )
            if len(alljob) == 0:
                errmsg = "No result found"
        else:
            alljob = Job.objects.all()

        context = {"alljob": alljob, "query": query, "errmsg": errmsg}
        return render(req, "dashboard.html", context)

def searchjob2(req):
    query = req.GET.get("q")
    errmsg = ""

    if req.user.is_authenticated:
        if query:
            alljob = Job.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)  | Q(salary__icontains=query)| Q(location__icontains=query)
            )
            if len(alljob) == 0:
                errmsg = "No result found"
        else:
            alljob = Job.objects.all()

        context = {"alljob": alljob, "query": query, "errmsg": errmsg}
        return render(req, "index.html", context)
    else:
        if query:
            alljob = Job.objects.filter(
                Q(title__icontains=query) | Q(company__icontains=query)  | Q(salary__icontains=query)| Q(location__icontains=query)
            )
            if len(alljob) == 0:
                errmsg = "No result found"
        else:
            alljob = Job.objects.all()

        context = {"alljob": alljob, "query": query, "errmsg": errmsg}
        return render(req, "index.html", context)
    
from django.shortcuts import render, get_object_or_404
from .models import Job, JobApplication


# SHOW JOB DETAIL
def job_detail(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    applicants = JobApplication.objects.filter(job=job)
    return render(request, 'job_detail.html', {'job': job, 'applicants': applicants})

from .forms import JobApplicationForm
from django.contrib import messages
 # FOR APPLY JOB
def apply_for_job(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    
    if request.user == job.user:
        messages.warning(request, 'You cannot apply for your own job posting.')
        return redirect('job_detail', jobid=jobid)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Associate the job with the job application before saving
            job_application = form.save(commit=False)
            job_application.job = job
            job_application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('apply_for_job', jobid=jobid)
    else:
        form = JobApplicationForm()
    
    return render(request, 'apply.html', {'job': job, 'form': form})


@login_required
# for showing job applicats who apply
def job_applicants(request, jobid=None):
    if jobid:
        job = get_object_or_404(Job, pk=jobid)
        applicants = JobApplication.objects.filter(job=job, applicant=request.user)
        return render(request, 'applicants.html', {'job': job, 'applicants': applicants})
    else:
        jobs = Job.objects.filter(user=request.user)  # Assuming there's a ForeignKey 'user' in the Job model
        all_applicants = {}
        for job in jobs:
            applicants = JobApplication.objects.filter(job=job)
            all_applicants[job] = applicants
        return render(request, 'all_applicants.html', {'all_applicants': all_applicants})
from django.contrib import messages  

# for any updation of register applicants status
def removeapplicant(request, id):
    applicant = get_object_or_404(JobApplication, pk=id)
    applicant.is_shortlisted = False
    applicant.save()
    messages.success(request, f'{applicant.name} status updated successfully!')
    return redirect(f"/applicants/")

# for removed register apllicants
def removeapplicants(request, id):
    applicant = get_object_or_404(JobApplication, pk=id)
    applicant_name = applicant.name
    applicant.delete()
    messages.success(request, f'{applicant_name} is removed successfully!')
    return redirect(f"/applicants/")

# save register applicants detail
def save_applicant(request, applicant_id):
    applicant = get_object_or_404(JobApplication, id=applicant_id)
    applicant.is_shortlisted = True
    applicant.save()
    messages.success(request, f'{applicant.name} application has been successfully saved.')
    return redirect(f'/applicants/')

def about_us(request):
    return render(request,'aboutus.html')
def help_center(request):
    return render(request,'helpcenter.html')
def carriar_advise(request):
    return render(request,'carriaradvise.html')
def privacy(request):
    return render(request,'privacy.html')
def hirepeople(request):
    if not request.user.is_authenticated:
        return redirect('signup')  # Assuming 'login' is the URL name for your login view
    else:
        return redirect('/index')

# from django.http import JsonResponse

# def set_hire_people_session(request):
#     if request.method == 'POST' and request.is_ajax():
#         request.session['hire_people_clicked'] = True
#         return JsonResponse({'message': 'Session updated successfully.'})
#     return JsonResponse({'error': 'Invalid request.'}, status=400)
    
# def submit_feedback(request):
#     if request.method == 'POST':
#         content = request.POST.get('feedback')
#         Feedback.objects.create(content=content)
#         return redirect('/')  # Redirect to homepage after submission
#     return redirect('/') 
    

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import JobApplication,Job

def send_email(request, applicant_id):
    applicant = JobApplication.objects.get(id=applicant_id)
    job = applicant.job  # Get the related Job object
    
    subject = f'Invitation for Interview - {job.title}'
    
    message = f'Congratulations {applicant.name},\n\n' \
              f'We are pleased to inform you that your application for the position of {job.title} at {job.company} has been shortlisted. ' \
              f'We would like to invite you for an interview to further discuss your qualifications and suitability for the role.\n\n' \
              f'Interview Details:\n' \
              f'- Date: [Interview Date]\n' \
              f'- Time: [Interview Time]\n' \
              f'- Location: [Interview Location]\n\n' \
              f'Please find attached the job description for your reference.\n\n' \
              f'Looking forward to meeting you.\n\n' \
              f'Best regards,\n' \
              f'PARVEZ ALAM\n' \
              f'HR manager  9068369495\n' \
              f'{job.company}'
    
    from_email = 'parvezalam9068@gmail.com'
    recipient_list = [applicant.email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    return redirect(f"/applicants/?email_sent={applicant.name}")

from .models import  SelectedCandidate
def save_applicants(request, applicant_id):
    applicant = JobApplication.objects.get(id=applicant_id)
    # Get the job related to this application
    job = applicant.job
    # You can add additional logic here such as checking if the applicant is already saved
    SelectedCandidate.objects.create(name=applicant.name, email=applicant.email, resume=applicant.resume, job=job)
    messages.success(request, f'{applicant.name} application has been successfully saved.')
    return redirect(f'/applicants/')

def selected_candidates(request):
    candidates = SelectedCandidate.objects.all()
    context = {
        'candidates': candidates,
    }
    return render(request, 'selected_candidates.html', context)

   

from django.core.mail import send_mail
from .models import SelectedCandidate
from django.shortcuts import redirect, reverse

def send_email_candidate(request, candidates_id):
    candidate = SelectedCandidate.objects.get(id=candidates_id)
    job = candidate.job  # Get the related Job object
    
    subject = f'Invitation for Interview - {job.title}'
    
    message = f'Congratulations {candidate.name},\n\n' \
              f'We are pleased to inform you that your application for the position of {job.title} at {job.company} has been shortlisted. ' \
              f'We would like to invite you for an interview to further discuss your qualifications and suitability for the role.\n\n' \
              f'Interview Details:\n' \
              f'- Date: [Interview Date]\n' \
              f'- Time: [Interview Time]\n' \
              f'- Location: [Interview Location]\n\n' \
              f'Please find attached the job description for your reference.\n\n' \
              f'Looking forward to meeting you.\n\n' \
              f'Best regards,\n' \
              f'Parvez Alam\n' \
              f'HR Manager\n' \
              f'Contact: 9068369495\n' \
              f'{job.company}'
    
    from_email = 'parvezalam9068@gmail.com'
    recipient_list = [candidate.email]
    
    send_mail(subject, message, from_email, recipient_list)
    messages.success(request, f'Email sent successfully to {candidate.name}')
    return redirect(reverse('selected_candidates') + f'?email_sent={candidate.name}')

def removecandidates(request, id):
    candidate = get_object_or_404(SelectedCandidate, pk=id)
    candidate_name = candidate.name
    candidate.delete()
    messages.success(request, f'Remove condidate {candidate.name} succesfully')
    return redirect('selected_candidates')

def save_job(request, job_id):
    if request.user.is_authenticated:
        # Check if the job is already saved by the user
        saved_jobs = SavedJob.objects.filter(user=request.user, job_id=job_id)
        if not saved_jobs.exists():
            saved_job = SavedJob(user=request.user, job_id=job_id)
            saved_job.save()
            # Add success message
            job_title = Job.objects.get(pk=job_id).title  # Get the job title
            messages.success(request, f'{job_title} is saved in your saved jobs!')
        # Redirect to the job detail page using the URL name 'job_detail' and passing job_id
        return redirect(reverse('job_detail', kwargs={'jobid': job_id}))
    else:
        return redirect('signup')
def job_save(request):
    if request.user.is_authenticated:
        # Fetch the user's saved jobs
        saved_jobs = SavedJob.objects.filter(user=request.user)
        return render(request, 'job_save.html', {'saved_jobs': saved_jobs})
    else:
        return redirect('signup')  # Redirect to login page if user
    

def job_detail2(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'job_detail.html', {'job': job})

def remove_saved_job(request, job_id):
    saved_jobs = SavedJob.objects.filter(job_id=job_id)
    
    # Check if any saved jobs with the given job_id exist
    if saved_jobs.exists():
        job_title = saved_jobs.first().job.title  # Get the title of the first saved job
        saved_jobs.delete()  # Delete all matching saved jobs
        messages.success(request, f'{job_title} is removed successfully!')
    else:
        messages.error(request, 'Job not found or already removed.')
    
    return redirect('job_save')
def user_applications(request):
    # Assuming the logged-in user is available in the request object
    user = request.user
    applications = JobApplication.objects.filter(name=user.username)
    return render(request, 'user_applications.html', {'applications': applications})

def remove_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        application.delete()
        messages.success(request, f'removed successfully!')
    return redirect('user_applications')












 