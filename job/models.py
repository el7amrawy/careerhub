from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import time

# Create your models here.

'''
 django model field : 
    - html widget
    - validation 
    - db size 
'''

JOB_TYPE = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Contract', 'Contract'),
    ('Freelance', 'Freelance'),
    ('Internship', 'Internship'),
)

JOB_LEVEL = (
    ('Entry Level', 'Entry Level'),
    ('Mid Level', 'Mid Level'),
    ('Senior Level', 'Senior Level'),
    ('Lead', 'Lead'),
)

def image_upload(instance, filename):
    imagename, extension = filename.split(".")
    return "jobs/%s.%s" % (int(time.time()), extension)

class Job(models.Model):  # table 
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # column
    company_name = models.CharField(max_length=100)
    company_description = models.TextField(max_length=1000, default='', blank=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=15, choices=JOB_TYPE)
    job_level = models.CharField(max_length=15, choices=JOB_LEVEL, default='Entry Level')
    description = models.TextField(max_length=2000)
    requirements = models.TextField(max_length=2000)
    responsibilities = models.TextField(max_length=2000)
    published_at = models.DateTimeField(auto_now=True)
    vacancy = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    salary = models.IntegerField(default=0)
    experience_min = models.IntegerField(default=0)
    experience_max = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    skills = models.ManyToManyField('Skill', related_name='jobs')
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return self.name

class Apply(models.Model):
    job = models.ForeignKey(Job, related_name='apply_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, related_name='applicant', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    website = models.URLField(blank=True)
    cv = models.FileField(upload_to='apply/')
    cover_letter = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('accepted', 'accepted')
    ], default='Pending')

    def __str__(self):
        return f"{self.name} - {self.job.title}"

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"

class Interview(models.Model):
    application = models.ForeignKey('Apply', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
