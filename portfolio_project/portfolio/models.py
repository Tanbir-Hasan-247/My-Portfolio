# portfolio/models.py
from django.db import models
from django.utils.text import slugify

class Experience(models.Model):
    # ... your existing Experience model ...
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    description = models.TextField(default='')
    logo_image = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.role} at {self.company}"


class Project(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True, null=True)
    # --- ADD THIS LINE ---
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# --- ADD THIS NEW MODEL ---
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    class Meta:
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title