from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CV, Experience, Education, Skill, Project, Certification, Achievement, Reference, CVTemplate 
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

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
    # Get all CVs for the current user, ordered by most recent
    user_cvs = CV.objects.filter(user=request.user).order_by('-created_at')
    
    # Get CV statistics
    total_cvs = user_cvs.count()
    recent_cv = user_cvs.first()  # Most recent CV
    
    context = {
        'user_cvs': user_cvs,
        'total_cvs': total_cvs,
        'recent_cv': recent_cv,
    }
    return render(request, 'cv_app/dashboard.html', context)

# Delete CV - protected, requires login
@login_required
def delete_cv(request, cv_id):
    try:
        cv = CV.objects.get(id=cv_id, user=request.user)
        cv_title = cv.title
        cv.delete()
        messages.success(request, f'CV "{cv_title}" has been deleted successfully.')
    except CV.DoesNotExist:
        messages.error(request, 'CV not found or you do not have permission to delete it.')
    
    return redirect('dashboard')

# Preview CV - protected, requires login
@login_required
def preview_cv(request, cv_id):
    try:
        cv = CV.objects.get(id=cv_id, user=request.user)
    except CV.DoesNotExist:
        messages.error(request, 'CV not found.')
        return redirect('dashboard')
    
    # Get template from URL parameter or use CV's template
    template_id = request.GET.get('template')
    if template_id:
        try:
            template = CVTemplate.objects.get(id=template_id)
        except CVTemplate.DoesNotExist:
            template = cv.template
    else:
        template = cv.template
    
    context = {
        'cv': cv,
        'template': template,
    }
    return render(request, 'cv_app/preview_cv.html', context)
@login_required
def duplicate_cv(request, cv_id):
    try:
        original_cv = CV.objects.get(id=cv_id, user=request.user)
        
        # Create new CV with "Copy" in title
        cv_count = CV.objects.filter(user=request.user).count() + 1
        new_cv = CV.objects.create(
            user=request.user,
            title=f"{original_cv.title} (Copy #{cv_count})",
            full_name=original_cv.full_name,
            email=original_cv.email,
            phone=original_cv.phone,
            location=original_cv.location,
            date_of_birth=original_cv.date_of_birth,
            gender=original_cv.gender,
            nationality=original_cv.nationality,
            languages=original_cv.languages,
            marital_status=original_cv.marital_status,
            linkedin_url=original_cv.linkedin_url,
            github_url=original_cv.github_url,
            professional_summary=original_cv.professional_summary,
            additional_info=original_cv.additional_info
        )
        
        # Duplicate experiences
        for experience in original_cv.experiences.all():
            Experience.objects.create(
                cv=new_cv,
                job_title=experience.job_title,
                company=experience.company,
                start_date=experience.start_date,
                end_date=experience.end_date,
                description=experience.description,
                achievements=experience.achievements
            )
        
        # Duplicate education
        for education in original_cv.educations.all():
            Education.objects.create(
                cv=new_cv,
                institution=education.institution,
                degree=education.degree,
                field_of_study=education.field_of_study,
                start_date=education.start_date,
                end_date=education.end_date,
                description=education.description
            )
        
        # Duplicate skills
        for skill in original_cv.skills.all():
            Skill.objects.create(
                cv=new_cv,
                name=skill.name,
                category=skill.category
            )
        
        # Duplicate projects
        for project in original_cv.projects.all():
            Project.objects.create(
                cv=new_cv,
                name=project.name,
                description=project.description,
                technologies=project.technologies,
                project_url=project.project_url,
                start_date=project.start_date,
                end_date=project.end_date
            )
        
        # Duplicate certifications
        for certification in original_cv.certifications.all():
            Certification.objects.create(
                cv=new_cv,
                name=certification.name,
                issuing_organization=certification.issuing_organization,
                issue_date=certification.issue_date,
                expiry_date=certification.expiry_date,
                credential_url=certification.credential_url
            )
        
        # Duplicate achievements
        for achievement in original_cv.achievements.all():
            Achievement.objects.create(
                cv=new_cv,
                title=achievement.title,
                issuing_organization=achievement.issuing_organization,
                date=achievement.date,
                description=achievement.description
            )
        
        # Duplicate references
        for reference in original_cv.references.all():
            Reference.objects.create(
                cv=new_cv,
                name=reference.name,
                position=reference.position,
                company=reference.company,
                email=reference.email,
                phone=reference.phone,
                relationship=reference.relationship
            )
        
        messages.success(request, f'CV "{original_cv.title}" duplicated successfully!')
        return redirect('edit_cv', cv_id=new_cv.id)
        
    except CV.DoesNotExist:
        messages.error(request, 'CV not found.')
        return redirect('dashboard')
# Create new CV - protected, requires login
@login_required
def create_cv(request):
    # Create a new CV for the user with a better default title
    cv_count = CV.objects.filter(user=request.user).count() + 1
    cv = CV.objects.create(
        user=request.user, 
        title=f"{request.user.username}'s CV #{cv_count}",
        full_name=request.user.get_full_name() or request.user.username
    )
    messages.success(request, 'Creating new CV!')
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
        
        # Handle template selection
        template_id = request.POST.get('cv_template')
        if template_id:
            try:
                cv.template = CVTemplate.objects.get(id=template_id)
            except CVTemplate.DoesNotExist:
                pass  # Keep existing template if invalid
        
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

        # Handle Skills
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
        
        print("CV with all sections and template saved successfully!")
        messages.success(request, 'CV updated successfully!')
        return redirect('edit_cv', cv_id=cv.id)
    
    # For GET requests, pre-fill the form with existing data
    context = {
        'cv': cv,
    }
    return render(request, 'cv_app/edit_cv.html', context)
@login_required
def download_cv_pdf(request, cv_id):
    try:
        cv = CV.objects.get(id=cv_id, user=request.user)
    except CV.DoesNotExist:
        messages.error(request, 'CV not found.')
        return redirect('dashboard')
    
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF object, using the buffer as its "file"
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for the 'Flowable' ob
    # jects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=6,
        textColor=colors.HexColor('#3498db')
    )
    
    normal_style = styles['Normal']
    
    # Header Section
    elements.append(Paragraph(cv.full_name or "Your Name", title_style))
    
    # Contact Information
    contact_info = []
    if cv.email:
        contact_info.append(cv.email)
    if cv.phone:
        contact_info.append(cv.phone)
    if cv.location:
        contact_info.append(cv.location)
    
    if contact_info:
        elements.append(Paragraph(" • ".join(contact_info), normal_style))
    
    # Links
    links = []
    if cv.linkedin_url:
        links.append("LinkedIn")
    if cv.github_url:
        links.append("GitHub")
    
    if links:
        elements.append(Paragraph(" • ".join(links), normal_style))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Professional Summary
    if cv.professional_summary:
        elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        elements.append(Paragraph(cv.professional_summary, normal_style))
        elements.append(Spacer(1, 0.2 * inch))
    
    # Work Experience
    if cv.experiences.all():
        elements.append(Paragraph("WORK EXPERIENCE", heading_style))
        for exp in cv.experiences.all():
            # Job title and company
            exp_title = f"<b>{exp.job_title}</b> - {exp.company}"
            elements.append(Paragraph(exp_title, normal_style))
            
            # Dates
            date_range = f"{exp.start_date} - {exp.end_date or 'Present'}"
            elements.append(Paragraph(date_range, normal_style))
            
            # Description
            if exp.description:
                elements.append(Paragraph(exp.description, normal_style))
            
            # Achievements
            if exp.achievements:
                elements.append(Paragraph(f"<b>Achievements:</b> {exp.achievements}", normal_style))
            
            elements.append(Spacer(1, 0.1 * inch))
        elements.append(Spacer(1, 0.2 * inch))
    
    # Education
    if cv.educations.all():
        elements.append(Paragraph("EDUCATION", heading_style))
        for edu in cv.educations.all():
            edu_title = f"<b>{edu.degree}</b> - {edu.institution}"
            elements.append(Paragraph(edu_title, normal_style))
            
            if edu.field_of_study:
                elements.append(Paragraph(f"Field of Study: {edu.field_of_study}", normal_style))
            
            date_range = f"{edu.start_date} - {edu.end_date}"
            elements.append(Paragraph(date_range, normal_style))
            
            if edu.description:
                elements.append(Paragraph(edu.description, normal_style))
            
            elements.append(Spacer(1, 0.1 * inch))
        elements.append(Spacer(1, 0.2 * inch))
    
    # Skills
    if cv.skills.all():
        elements.append(Paragraph("SKILLS", heading_style))
        
        # Group skills by category
        skills_by_category = {}
        for skill in cv.skills.all():
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill.name)
        
        for category, skill_list in skills_by_category.items():
            category_name = category.replace('_', ' ').title()
            skills_text = f"<b>{category_name}:</b> {', '.join(skill_list)}"
            elements.append(Paragraph(skills_text, normal_style))
        
        elements.append(Spacer(1, 0.2 * inch))
    
    # Projects
    if cv.projects.all():
        elements.append(Paragraph("PROJECTS", heading_style))
        for project in cv.projects.all():
            elements.append(Paragraph(f"<b>{project.name}</b>", normal_style))
            
            if project.technologies:
                elements.append(Paragraph(f"Technologies: {project.technologies}", normal_style))
            
            if project.description:
                elements.append(Paragraph(project.description, normal_style))
            
            elements.append(Spacer(1, 0.1 * inch))
        elements.append(Spacer(1, 0.2 * inch))
    
    # Certifications
    if cv.certifications.all():
        elements.append(Paragraph("CERTIFICATIONS", heading_style))
        for cert in cv.certifications.all():
            cert_text = f"<b>{cert.name}</b> - {cert.issuing_organization}"
            if cert.issue_date:
                cert_text += f" ({cert.issue_date})"
            elements.append(Paragraph(cert_text, normal_style))
        elements.append(Spacer(1, 0.2 * inch))
    
    # Achievements
    if cv.achievements.all():
        elements.append(Paragraph("ACHIEVEMENTS", heading_style))
        for achievement in cv.achievements.all():
            achievement_text = f"<b>{achievement.title}</b>"
            if achievement.issuing_organization:
                achievement_text += f" - {achievement.issuing_organization}"
            if achievement.date:
                achievement_text += f" ({achievement.date})"
            elements.append(Paragraph(achievement_text, normal_style))
            
            if achievement.description:
                elements.append(Paragraph(achievement.description, normal_style))
            
            elements.append(Spacer(1, 0.1 * inch))
    
    # Build PDF
    doc.build(elements)
    
    # File response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.title.replace(" ", "_")}.pdf"'
    
    return response
