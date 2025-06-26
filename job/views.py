from django.shortcuts import redirect, render, get_object_or_404
from .models import Job, Apply, SavedJob, Category
from django.core.paginator import Paginator
from .form import ApplyForm , JobForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .filters import JobFilter
from accounts.models import Profile, Activity
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SetInterviewForm
from .models import Interview, Notification

# Create your views here.

def job_list(request):
    # Order jobs by is_featured (True first) and then by published_at (newest first)
    job_list = Job.objects.filter(is_active=True).order_by('-is_featured', '-published_at')

    ## filters
    myfilter = JobFilter(request.GET,queryset=job_list)
    job_list = myfilter.qs

    paginator = Paginator(job_list, 5) # Show 5 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique job locations for the filter dropdown
    locations = Job.objects.values_list('location', flat=True).distinct().order_by('location')

    # Get saved jobs for authenticated users
    user_saved_jobs = []
    if request.user.is_authenticated:
        user_saved_jobs = SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True)

    context = {
        'jobs': page_obj, 
        'myfilter': myfilter, 
        'locations': locations,
        'user_saved_jobs': user_saved_jobs
    }
    return render(request,'job/job_list.html',context)

@login_required
def job_detail(request, slug):
    job_detail = Job.objects.get(slug=slug)

    # Check if job is saved by current user
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job_detail).exists()

    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.job = job_detail
            myform.applicant = request.user
            myform.save()
            
            # Create activity record
            try:
                Activity.objects.create(
                    user=request.user,
                    activity_type='applied',
                    job=job_detail,
                    details=f'Applied for {job_detail.title} at {job_detail.company_name}'
                )
                messages.success(request, 'Application submitted successfully!')
            except Exception as e:
                messages.error(request, f'Error creating activity: {str(e)}')
            
            return redirect('/jobs/')  # Redirect to job list page instead

    else:
        form = ApplyForm()

    context = {
        'job': job_detail, 
        'form1': form,
        'is_saved': is_saved,
        'user_saved_jobs': [job_detail.id] if is_saved else []
    }
    return render(request, 'job/job_detail.html', context)

@login_required
def company_dashboard(request):
    # Check if user is a company
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != 'company':
        return redirect('/jobs/')
    
    # Get company's posted jobs
    company_jobs = Job.objects.filter(owner=request.user)
    
    # Calculate statistics
    active_jobs_count = company_jobs.filter(is_active=True).count()
    total_applications = Apply.objects.filter(job__in=company_jobs).count()
    new_applications = Apply.objects.filter(
        job__in=company_jobs,
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()
    
    # Get recent applications
    recent_applications = Apply.objects.filter(
        job__in=company_jobs
    ).order_by('-created_at')[:5]
    
    context = {
        'jobs': company_jobs,
        'profile': profile,
        'active_jobs_count': active_jobs_count,
        'total_applications': total_applications,
        'new_applications': new_applications,
        'recent_applications': recent_applications
    }
    return render(request, 'job/company_dashboard.html', context)

@login_required
def add_job(request):
    # Check if user is a company
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != 'company':
        return redirect('jobs:job_list')
    
    if request.method=='POST':
        form = JobForm(request.POST , request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.company_name = request.user.username  # Use username as company name
            myform.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:company_dashboard')
    else:
        form = JobForm(initial={'company_name': request.user.username})
    
    # Get all categories and print them for debugging
    categories = Category.objects.all()
    print("Available categories:", [c.name for c in categories])
    
    return render(request, 'job/add_job.html', {
        'form': form,
        'categories': categories
    })

@login_required
def edit_job(request, id):
    # Get the job and verify ownership
    job = Job.objects.get(id=id)
    if job.owner != request.user:
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('job:job_list')
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job:job_detail', slug=job.slug)
    else:
        form = JobForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
        'categories': Job.objects.values_list('category', flat=True).distinct()
    }
    return render(request, 'job/edit_job.html', context)

@require_POST
@login_required
def toggle_wishlist(request, job_id):
    job = Job.objects.get(id=job_id)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    
    if created:
        messages.success(request, f'{job.title} added to your wishlist!')
    else:
        saved_job.delete()
        messages.success(request, f'{job.title} removed from your wishlist.')
    
    return JsonResponse({'status': 'success'})

@login_required
def set_interview(request, application_id):
    application = get_object_or_404(Apply, id=application_id)
    if request.method == 'POST':
        form = SetInterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            # Send notification to applicant
            notes_text = f" Notes: {interview.notes}" if interview.notes else ""
            Notification.objects.create(
                user=application.applicant,
                message=f"🎯 Interview Scheduled!\n\n📋 Job: {application.job.title}\n📅 Date: {interview.date}\n⏰ Time: {interview.time}\n📍 Location: {interview.location}{notes_text}"
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@require_POST
@login_required
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

@require_POST
@login_required
def delete_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id, user=request.user)
        activity.delete()
        return JsonResponse({'status': 'success'})
    except Activity.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Activity not found'}, status=404)

@require_POST
@login_required
def clear_activities(request):
    try:
        Activity.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)