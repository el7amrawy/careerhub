from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]