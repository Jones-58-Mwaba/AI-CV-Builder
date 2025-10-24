from django.db import models
from django.contrib.auth.models import User

class CV(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My CV")
    
    # Basic Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    
    # Personal Details
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=255, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    additional_info = models.TextField(blank=True)
    
    # Professional
    professional_summary = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return f"{self.full_name} - {self.title}"

class Experience(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    
    def _str_(self):
        return f"{self.job_title} at {self.company}"

class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    def _str_(self):
        return f"{self.degree} at {self.institution}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical Skills'),
        ('soft', 'Soft Skills'), 
        ('languages', 'Languages'),
        ('tools', 'Tools & Technologies'),
    ]
    
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technical')
    
    def _str_(self):
        return f"{self.name} ({self.category})"

class Project(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=200, blank=True)
    project_url = models.URLField(blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
    
    def _str_(self):
        return self.name

class Certification(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.CharField(max_length=20, blank=True)
    expiry_date = models.CharField(max_length=20, blank=True)
    credential_url = models.URLField(blank=True)
    
    def _str_(self):
        return self.name

class Achievement(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    def _str_(self):
        return self.title

class Reference(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    
    def _str_(self):
        return f"{self.name} - {self.position}"
