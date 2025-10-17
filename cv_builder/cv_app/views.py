from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CV, Experience, Education, Skill, Project, Certification, Achievement

# Home page - public landing page
def home(request):
    return render(request, 'cv_app/home.html')

# User registration/signup
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            except:
                messages.error(request, 'Username already exists')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'cv_app/signup.html')

# User login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'cv_app/login.html')

# User logout
def logout_view(request):
    logout(request)
    return redirect('home')

# User dashboard - protected, requires login
@login_required
def dashboard(request):
    return render(request, 'cv_app/dashboard.html')

# Create new CV - protected, requires login
@login_required
def create_cv(request):
    # Create a new CV for the user
    cv = CV.objects.create(user=request.user, title=f"{request.user.username}'s CV")
    return redirect('edit_cv', cv_id=cv.id)

# Edit existing CV - protected, requires login
@login_required
def edit_cv(request, cv_id):
    try:
        cv = CV.objects.get(id=cv_id, user=request.user)
    except CV.DoesNotExist:
        return redirect('dashboard')
    
    if request.method == 'POST':
        print("Form submitted!")  # Debug line
        
        # Update CV basic information
        cv.full_name = request.POST.get('full_name', '')
        cv.email = request.POST.get('email', '')
        cv.phone = request.POST.get('phone', '')
        cv.location = request.POST.get('location', '')
        
        # Handle date field properly
        date_of_birth = request.POST.get('date_of_birth')
        cv.date_of_birth = date_of_birth if date_of_birth else None
        
        cv.gender = request.POST.get('gender', '')
        cv.nationality = request.POST.get('nationality', '')
        cv.languages = request.POST.get('languages', '')
        cv.marital_status = request.POST.get('marital_status', '')
        cv.linkedin_url = request.POST.get('linkedin', '')
        cv.github_url = request.POST.get('portfolio', '')
        cv.professional_summary = request.POST.get('professional_summary', '')
        cv.additional_info = request.POST.get('additional_info', '')
        
        cv.save()
        
        # Handle Work Experience
        job_titles = request.POST.getlist('experience_job_title')
        companies = request.POST.getlist('experience_company')
        start_dates = request.POST.getlist('experience_start_date')
        end_dates = request.POST.getlist('experience_end_date')
        descriptions = request.POST.getlist('experience_description')
        achievements = request.POST.getlist('experience_achievements')
        
        existing_experiences = list(cv.experiences.all())
        
        for i in range(len(job_titles)):
            if job_titles[i] and companies[i]:
                if i < len(existing_experiences):
                    experience = existing_experiences[i]
                    experience.job_title = job_titles[i]
                    experience.company = companies[i]
                    experience.start_date = start_dates[i]
                    experience.end_date = end_dates[i]
                    experience.description = descriptions[i]
                    experience.achievements = achievements[i]
                    experience.save()
                else:
                    Experience.objects.create(
                        cv=cv,
                        job_title=job_titles[i],
                        company=companies[i],
                        start_date=start_dates[i],
                        end_date=end_dates[i],
                        description=descriptions[i],
                        achievements=achievements[i]
                    )
        
        if len(job_titles) < len(existing_experiences):
            for i in range(len(job_titles), len(existing_experiences)):
                existing_experiences[i].delete()

        # NEW: Handle Education
        institutions = request.POST.getlist('education_institution')
        degrees = request.POST.getlist('education_degree')
        fields_of_study = request.POST.getlist('education_field_of_study')
        education_start_dates = request.POST.getlist('education_start_date')
        education_end_dates = request.POST.getlist('education_end_date')
        education_descriptions = request.POST.getlist('education_description')
        
        existing_educations = list(cv.educations.all())
        
        for i in range(len(institutions)):
            if institutions[i] and degrees[i]:  # Only process if required fields are filled
                if i < len(existing_educations):
                    # Update existing education
                    education = existing_educations[i]
                    education.institution = institutions[i]
                    education.degree = degrees[i]
                    education.field_of_study = fields_of_study[i]
                    education.start_date = education_start_dates[i]
                    education.end_date = education_end_dates[i]
                    education.description = education_descriptions[i]
                    education.save()  # ← USING .save()!
                else:
                    # Create new education
                    Education.objects.create(
                        cv=cv,
                        institution=institutions[i],
                        degree=degrees[i],
                        field_of_study=fields_of_study[i],
                        start_date=education_start_dates[i],
                        end_date=education_end_dates[i],
                        description=education_descriptions[i]
                    )
        
        # Delete any extra educations that are no longer needed
        if len(institutions) < len(existing_educations):
            for i in range(len(institutions), len(existing_educations)):
                existing_educations[i].delete()
        
        print("CV, Experiences, and Education saved successfully!")
        messages.success(request, 'CV updated successfully!')
        return redirect('edit_cv', cv_id=cv.id)
    
    # For GET requests, pre-fill the form with existing data
    context = {
        'cv': cv,
    }
    return render(request, 'cv_app/edit_cv.html', context)