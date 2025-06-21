"""
URL configuration for petsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from portalapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("index/", views.index, name="index"),
   
    path("registerjob/", views.registerjob, name="registerjob"),
    path("removejob/<jobid>", views.removejob, name="removejob"),
    path("updatejob/<jobid>", views.updatejob, name="updatejob"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("hirepeople/", views.hirepeople, name="hirepeople"),
     path(
        "request_password_reset/",
        views.request_password_reset,
        name="request_password_reset",
    ),
    path("reset_password/<username>/", views.reset_password, name="reset_password"),
   
    path("searchjob", views.searchjob, name="searchjob"),
    path("searchjob2", views.searchjob2, name="searchjob2"),
    path('job/<int:jobid>/', views.job_detail, name='job_detail'),
    path('job/<int:jobid>/apply/', views.apply_for_job, name='apply_for_job'),
    path('job/<int:jobid>/applicants/', views.job_applicants, name='job_applicants'),
    path('applicants/', views.job_applicants, name='all_job_applicants'),
    # path('submit-feedback/',views.submit_feedback, name='submit_feedback'),
    path('removeapplicant/<int:id>/', views.removeapplicant, name='removeapplicant'),
    path('removeapplicants/<int:id>/', views.removeapplicants, name='removeapplicants'),
    path('aboutus.html', views.about_us, name='about_us'),
    path('helpcenter.html', views.help_center, name='help_center'),
    path('carriaradvise.html', views.carriar_advise, name='carriar_advise'),
    path('privacy.html', views.privacy, name='privacy'),
    path('send_email/<int:applicant_id>/', views.send_email, name='send_email'),
    path('social-auth',include("social_django.urls",namespace="social")),
    path('saveapplicant/<int:applicant_id>/', views.save_applicant, name='save_applicant'),
    path('saveapplicants/<int:applicant_id>/', views.save_applicants, name='save_applicants'),
     path('selectedcandidates/', views.selected_candidates, name='selected_candidates'),
    path('send_email_candidate/<int:candidates_id>/',  views.send_email_candidate, name='send_email_candidate'),
    path('removecandidates/<int:id>/', views.removecandidates, name='removecandidates'),
     path('save_job/<int:job_id>/', views.save_job, name='save_job'),
    path('job_save/', views.job_save, name='job_save'),
    path('job-detail2/<int:job_id>/', views.job_detail2, name='job_detail2'),
    path('remove_saved_job/<int:job_id>/', views.remove_saved_job, name='remove_saved_job'),
    path('my_applications/', views.user_applications, name='user_applications'),
      path('remove_application/<int:application_id>/', views.remove_application, name='remove_application'),

      path('index/aboutus.html', views.about_us, name='about_us'),
    path('index/helpcenter.html', views.help_center, name='help_center'),
    path('index/carriaradvise.html', views.carriar_advise, name='carriar_advise'),
    path('index/privacy.html', views.privacy, name='privacy'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls.py

