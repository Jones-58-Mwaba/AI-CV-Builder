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
    
    # Handle form submission
    if request.method == 'POST':
        # Update personal information
        cv.full_name = request.POST.get('full_name', '')
        cv.email = request.POST.get('email', '')
        cv.phone = request.POST.get('phone', '')
        cv.location = request.POST.get('location', '')
        cv.linkedin = request.POST.get('linkedin', '')
        cv.professional_summary = request.POST.get('professional_summary', '')
        cv.save()
        
        # Handle experiences
        company = request.POST.get('company')
        position = request.POST.get('position')
        if company and position:  # Only save if required fields exist
            Experience.objects.create(
                cv=cv,
                company=company,
                job_title=position,
                start_date=request.POST.get('start_date', ''),
                end_date=request.POST.get('end_date', ''),
                description=request.POST.get('description', '')
            )
        
        return redirect('edit_cv', cv_id=cv.id)
    
    return render(request, 'cv_app/edit_cv.html', {'cv': cv})