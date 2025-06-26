from django.urls import include, path

from . import views
from . import api 


app_name='job'

urlpatterns = [
    path('',views.job_list , name='job_list'),
    path('add',views.add_job , name='add_job'),
    path('edit/<int:id>',views.edit_job , name='edit_job'),
    path('<str:slug>',views.job_detail , name='job_detail'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('wishlist/toggle/<int:job_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('set-interview/<int:application_id>/', views.set_interview, name='set_interview'),
    path('delete-notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('delete-activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('clear-activities/', views.clear_activities, name='clear_activities'),

    ## api
    path('api/jobs',api.job_list_api , name='job_list_api'),
    path('api/jobs/<int:id>',api.job_detail_api , name='job_detail_api'),

    ## class based views
    path('api/v2/jobs',api.JobListApi.as_view() , name='job_list_api'),
    path('api/v2/jobs/<int:id>',api.JobDetail.as_view() , name='job_detail_api'),
]