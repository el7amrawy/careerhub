from django.shortcuts import render
from job.models import Job, Category
from job.filters import JobFilter
from django.db.models import Count

# Create your views here.

def home(request):
    # Get featured jobs (jobs marked as featured)
    featured_jobs = Job.objects.filter(is_featured=True)[:6]  # Get up to 6 featured jobs
    
    # Get specific categories for popular categories section
    specific_categories_names = ['Web Development', 'Mobile', 'Marketing']
    specific_categories = Category.objects.filter(name__in=specific_categories_names)
    
    # Get 3 random categories, excluding the specific ones
    random_categories = Category.objects.exclude(name__in=specific_categories_names).order_by('?')[:3]
    
    # Combine all categories
    categories = list(specific_categories) + list(random_categories)

    # Get popular job titles from actual posted jobs
    popular_job_titles = Job.objects.values('title').annotate(
        count=Count('title')
    ).order_by('-count')[:7]  # Get top 7 most common job titles

    # Initialize JobFilter for the home page search form
    home_search_filter = JobFilter(request.GET, queryset=Job.objects.all())

    context = {
        'featured_jobs': featured_jobs,
        'categories': categories,
        'home_search_filter': home_search_filter,
        'popular_job_titles': popular_job_titles,
    }
    return render(request, 'home/index.html', context)
