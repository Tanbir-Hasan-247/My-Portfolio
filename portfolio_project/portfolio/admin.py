# portfolio/admin.py
from django.contrib import admin
from .models import Experience, Project, BlogPost # Add BlogPost

# Register your models here.
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(BlogPost) # Register the new model