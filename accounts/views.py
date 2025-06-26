from django.shortcuts import redirect, render
from .forms import SignupForm , UserForm , ProfileForm
from django.contrib.auth import authenticate, login
from .models import Profile, Activity
from job.models import Apply, SavedJob, Notification
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            profile = Profile.objects.get(user=user)
            if profile.user_type == 'company':
                return redirect('jobs:company_dashboard')
            else:
                return redirect('jobs:job_list')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create user using form.save()
            user = form.save()
            user_type = form.cleaned_data['user_type']

            # Create profile for the new user
            # Check if a profile already exists (in case of a signal)
            profile, created = Profile.objects.get_or_create(user=user, defaults={'user_type': user_type})
            if not created:
                 # If profile already existed, ensure user_type is set
                 profile.user_type = user_type
                 profile.save()

            # Log the user in
            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            
            # Redirect based on user type
            if user_type == 'company':
                return redirect('jobs:company_dashboard')
            else:
                return redirect('jobs:job_list')
    else:
        form = SignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    # Filter out activities where the job has been deleted
    activity = Activity.objects.filter(user=request.user).exclude(job__isnull=True)
    
    # Get saved jobs for job seekers
    saved_jobs = []
    if profile.user_type == 'job_seeker':
        saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    # Get notifications for the user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    
    
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'activity': activity,
        'saved_jobs': saved_jobs,
        'notifications': notifications,
    })

def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method=='POST':
        userform = UserForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            messages.success(request, 'Profile has been updated successfully!')
            return redirect('jobs:company_dashboard')

    else :
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request,'accounts/profile_edit.html',{'userform':userform , 'profileform':profileform})