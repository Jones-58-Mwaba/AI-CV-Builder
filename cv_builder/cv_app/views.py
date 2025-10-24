from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CV, Experience, Education, Skill, Project, Certification, Achievement, Reference

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

        # Handle Education
        institutions = request.POST.getlist('education_institution')
        degrees = request.POST.getlist('education_degree')
        fields_of_study = request.POST.getlist('education_field_of_study')
        education_start_dates = request.POST.getlist('education_start_date')
        education_end_dates = request.POST.getlist('education_end_date')
        education_descriptions = request.POST.getlist('education_description')
        
        existing_educations = list(cv.educations.all())
        
        for i in range(len(institutions)):
            if institutions[i] and degrees[i]:
                if i < len(existing_educations):
                    education = existing_educations[i]
                    education.institution = institutions[i]
                    education.degree = degrees[i]
                    education.field_of_study = fields_of_study[i]
                    education.start_date = education_start_dates[i]
                    education.end_date = education_end_dates[i]
                    education.description = education_descriptions[i]
                    education.save()
                else:
                    Education.objects.create(
                        cv=cv,
                        institution=institutions[i],
                        degree=degrees[i],
                        field_of_study=fields_of_study[i],
                        start_date=education_start_dates[i],
                        end_date=education_end_dates[i],
                        description=education_descriptions[i]
                    )
        
        if len(institutions) < len(existing_educations):
            for i in range(len(institutions), len(existing_educations)):
                existing_educations[i].delete()

        # NEW: Handle Skills
        skill_names = request.POST.getlist('skill_name')
        skill_categories = request.POST.getlist('skill_category')
        
        existing_skills = list(cv.skills.all())
        
        for i in range(len(skill_names)):
            if skill_names[i] and skill_categories[i]:
                if i < len(existing_skills):
                    # Update existing skill
                    skill = existing_skills[i]
                    skill.name = skill_names[i]
                    skill.category = skill_categories[i]
                    skill.save()
                else:
                    # Create new skill
                    Skill.objects.create(
                        cv=cv,
                        name=skill_names[i],
                        category=skill_categories[i]
                    )
        
        # Delete any extra skills that are no longer needed
        if len(skill_names) < len(existing_skills):
            for i in range(len(skill_names), len(existing_skills)):
                existing_skills[i].delete()
                
                            
                                # Handle Projects
        project_names = request.POST.getlist('project_name')
        project_technologies = request.POST.getlist('project_technologies')
        project_urls = request.POST.getlist('project_url')
        project_start_dates = request.POST.getlist('project_start_date')
        project_end_dates = request.POST.getlist('project_end_date')
        project_descriptions = request.POST.getlist('project_description')

        existing_projects = list(cv.projects.all())

        for i in range(len(project_names)):
            if project_names[i]:  # Only create if project name exists
                if i < len(existing_projects):
                    # Update existing project
                    project = existing_projects[i]
                    project.name = project_names[i]
                    project.technologies = project_technologies[i]
                    project.project_url = project_urls[i]
                    project.start_date = project_start_dates[i]
                    project.end_date = project_end_dates[i]
                    project.description = project_descriptions[i]
                    project.save()
                else:
                    # Create new project
                    Project.objects.create(
                        cv=cv,
                        name=project_names[i],
                        technologies=project_technologies[i],
                        project_url=project_urls[i],
                        start_date=project_start_dates[i],
                        end_date=project_end_dates[i],
                        description=project_descriptions[i]
                    )

        # Delete any extra projects that are no longer needed
        if len(project_names) < len(existing_projects):
            for i in range(len(project_names), len(existing_projects)):
                existing_projects[i].delete()
                
        
        # Handle Certifications
        certification_names = request.POST.getlist('certification_name')
        certification_organizations = request.POST.getlist('certification_organization')
        certification_issue_dates = request.POST.getlist('certification_issue_date')
        certification_expiry_dates = request.POST.getlist('certification_expiry_date')
        certification_urls = request.POST.getlist('certification_url')
        
        existing_certifications = list(cv.certifications.all())
        
        for i in range(len(certification_names)):
            if certification_names[i] and certification_organizations[i]:
                if i < len(existing_certifications):
                    # Update existing certification
                    certification = existing_certifications[i]
                    certification.name = certification_names[i]
                    certification.issuing_organization = certification_organizations[i]
                    certification.issue_date = certification_issue_dates[i]
                    certification.expiry_date = certification_expiry_dates[i]
                    certification.credential_url = certification_urls[i]
                    certification.save()
                else:
                    # Create new certification
                    Certification.objects.create(
                        cv=cv,
                        name=certification_names[i],
                        issuing_organization=certification_organizations[i],
                        issue_date=certification_issue_dates[i],
                        expiry_date=certification_expiry_dates[i],
                        credential_url=certification_urls[i]
                    )
        
        # Delete any extra certifications that are no longer needed
        if len(certification_names) < len(existing_certifications):
            for i in range(len(certification_names), len(existing_certifications)):
                existing_certifications[i].delete()   
                
        # Handle Achievements
        achievement_titles = request.POST.getlist('achievement_title')
        achievement_organizations = request.POST.getlist('achievement_organization')
        achievement_dates = request.POST.getlist('achievement_date')
        achievement_descriptions = request.POST.getlist('achievement_description')
        
        existing_achievements = list(cv.achievements.all())
        
        for i in range(len(achievement_titles)):
            if achievement_titles[i]:  # Only create if title exists
                if i < len(existing_achievements):
                    # Update existing achievement
                    achievement = existing_achievements[i]
                    achievement.title = achievement_titles[i]
                    achievement.issuing_organization = achievement_organizations[i]
                    achievement.date = achievement_dates[i]
                    achievement.description = achievement_descriptions[i]
                    achievement.save()
                else:
                    # Create new achievement
                    Achievement.objects.create(
                        cv=cv,
                        title=achievement_titles[i],
                        issuing_organization=achievement_organizations[i],
                        date=achievement_dates[i],
                        description=achievement_descriptions[i]
                    )
        
        # Delete any extra achievements that are no longer needed
        if len(achievement_titles) < len(existing_achievements):
            for i in range(len(achievement_titles), len(existing_achievements)):
                existing_achievements[i].delete()   
                
        # Handle References
        reference_names = request.POST.getlist('reference_name')
        reference_positions = request.POST.getlist('reference_position')
        reference_companies = request.POST.getlist('reference_company')
        reference_emails = request.POST.getlist('reference_email')
        reference_phones = request.POST.getlist('reference_phone')
        reference_relationships = request.POST.getlist('reference_relationship')
        
        existing_references = list(cv.references.all())
        
        for i in range(len(reference_names)):
            if reference_names[i]:  # Only create if name exists
                if i < len(existing_references):
                    # Update existing reference
                    reference = existing_references[i]
                    reference.name = reference_names[i]
                    reference.position = reference_positions[i]
                    reference.company = reference_companies[i]
                    reference.email = reference_emails[i]
                    reference.phone = reference_phones[i]
                    reference.relationship = reference_relationships[i]
                    reference.save()
                else:
                    # Create new reference
                    Reference.objects.create(
                        cv=cv,
                        name=reference_names[i],
                        position=reference_positions[i],
                        company=reference_companies[i],
                        email=reference_emails[i],
                        phone=reference_phones[i],
                        relationship=reference_relationships[i]
                    )
        
        # Delete any extra references that are no longer needed
        if len(reference_names) < len(existing_references):
            for i in range(len(reference_names), len(existing_references)):
                existing_references[i].delete()          
        
        
        print("CV, Experiences, Education, Skills, Projects, Certification, Achievements and References saved successfully!")
        messages.success(request, 'Your resume is edited successfully!')
        return redirect('edit_cv', cv_id=cv.id)
    
    # For GET requests, pre-fill the form with existing data
    context = {
        'cv': cv,
    }
    return render(request, 'cv_app/edit_cv.html', context)