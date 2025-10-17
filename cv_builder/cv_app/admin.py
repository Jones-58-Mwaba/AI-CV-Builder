from django.contrib import admin
from .models import CV, Experience, Education, Skill, Project, Certification, Achievement

# Register all models
admin.site.register(CV)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Certification)
admin.site.register(Achievement)