from django.contrib import admin
from .models import Job,JobApplication,Feedback,SavedJob

class JobAdmin(admin.ModelAdmin):
    list_display = ('jobid','user','title', 'company', 'location', 'job_type', 'salary','created_at','experience','days','nop')

 

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job','name', 'email', 'resume','id','is_shortlisted')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('content','created_at')
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user','job')


class SelectedCandidate(admin.ModelAdmin):
    list_display=('id','job','name','email','resume')
   

admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(SavedJob, SavedJobAdmin)

