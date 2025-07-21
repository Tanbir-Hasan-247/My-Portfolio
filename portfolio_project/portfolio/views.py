# portfolio/views.py
from django.shortcuts import render, get_object_or_404
from .models import Experience, Project, BlogPost

def home(request):
    experiences = Experience.objects.all().order_by('-start_date')
    # Separate the featured project from the rest
    all_projects = Project.objects.all().order_by('display_order')
    featured_project = all_projects.first()
    other_projects = all_projects[1:]

    context = {
        'experiences': experiences,
        'featured_project': featured_project,
        'other_projects': other_projects,
    }
    return render(request, 'portfolio/index.html', context)

# --- ADD THESE TWO NEW VIEWS ---

def blog_list(request):
    posts = BlogPost.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'portfolio/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'portfolio/blog_detail.html', context)