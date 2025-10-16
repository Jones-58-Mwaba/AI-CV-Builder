from django.db import models
from django.contrib.auth.models import User

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Professional CV")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 1. Contact Information
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    
    # 2. Professional Summary
    professional_summary = models.TextField(blank=True)
    
    def _str_(self):
        return f"{self.user.username} - {self.title}"

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
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    relevant_coursework = models.TextField(blank=True)
    
    def _str_(self):
        return f"{self.degree} at {self.institution}"

class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True)  # Technical, Soft, Language
    proficiency = models.CharField(max_length=20, blank=True)  # Beginner, Intermediate, Expert
    
    def _str_(self):
        return self.name

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