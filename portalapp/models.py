from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    jobid = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    DAYS_CHOICES = (
        ('monday-friday', 'Monday-Friday'),
        ('monday-saturday', 'Monday-Saturday'),
    )
    days = models.CharField(max_length=50, choices=DAYS_CHOICES,null=True)

    EXPERIENCE_CHOICES = (
        ('0-1 years', '0-1 years'),
        ('1-3 years', '1-3 years'),
        ('3-5 years', '3-5 years'),
        ('5-above years', '5 years and above'),
    )
    nop = models.DecimalField(max_digits=10,decimal_places=0,null=True)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    

class JobApplication(models.Model):
   job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
   name = models.CharField(max_length=100)
   email = models.EmailField()
   resume = models.FileField(upload_to='resumes/')
   id = models.AutoField(primary_key=True)
   is_shortlisted = models.BooleanField(default=False)

class Feedback(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SelectedCandidate(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/') 


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # Assuming you have a Job model

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"




