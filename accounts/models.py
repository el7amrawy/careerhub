from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from job.models import Job

# Create your models here.

USER_TYPE_CHOICES = (
    ('company', 'Company'),
    ('job_seeker', 'Job Seeker'),
)

ACTIVITY_TYPES = (
    ('applied', 'Applied to Job'),
    ('posted', 'Posted a Job'),
    ('updated', 'Updated Profile'),
    ('saved', 'Saved a Job'),
    ('viewed', 'Viewed a Job'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
    city = models.ForeignKey('City', related_name='user_city', on_delete=models.CASCADE , blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile/')
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"

## create new user ---> create new empty profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


