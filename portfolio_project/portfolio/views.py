# portfolio/views.py
from django.shortcuts import render, get_object_or_404
from .models import Experience, Project, BlogPost
from django.core.cache import cache
from . import utils


def home(request):
    experiences = Experience.objects.all().order_by("-start_date")
    all_projects = Project.objects.all().order_by("display_order")
    featured_project = all_projects.first()
    other_projects = all_projects[1:]

    # --- Usernames for Coding Profiles ---
    cf_username = "Tanbir_hasan"  # Replace with your Codeforces handle
    cc_username = "tanbir_hasan19"  # Replace with your CodeChef handle
    leetcode_username = "Tanbir_hasan"  # Replace with your LeetCode handle

    # --- Fetching and Caching Logic ---
    codeforces_data = cache.get(f"codeforces_{cf_username}")
    if not codeforces_data:
        codeforces_data = utils.get_codeforces_data(cf_username)
        cache.set(f"codeforces_{cf_username}", codeforces_data, 3600)

    codechef_data = cache.get(f"codechef_{cc_username}")
    if not codechef_data:
        codechef_data = utils.get_codechef_data(cc_username)
        cache.set(f"codechef_{cc_username}", codechef_data, 3600)

    leetcode_data = cache.get(f"leetcode_{leetcode_username}")
    if not leetcode_data:
        leetcode_data = utils.get_leetcode_data(leetcode_username)
        cache.set(f"leetcode_{leetcode_username}", leetcode_data, 3600)

    context = {
        "experiences": experiences,
        "featured_project": featured_project,
        "other_projects": other_projects,
        "codeforces_data": codeforces_data,
        "codechef_data": codechef_data,
        "leetcode_data": leetcode_data,
    }
    return render(request, "portfolio/index.html", context)


def blog_list(request):
    posts = BlogPost.objects.all()
    print(f"DEBUG: Found {posts.count()} blog posts in the database.")  # Debug print
    context = {
        "posts": posts,
    }
    return render(request, "portfolio/blog_list.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    context = {
        "post": post,
    }
    return render(request, "portfolio/blog_detail.html", context)
