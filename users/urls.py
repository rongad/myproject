from django.urls import path
from django.contrib.auth import views as auth_views

from users import views_disciplinary, views_profile
from . import views



urlpatterns = [
    path('', views.login_view, name='login'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('incidents/', views_disciplinary.IncidentView.as_view(), name='incident_list'),
    path('incidents/new', views_disciplinary.IncidentCreateView.as_view(), name='incident_new'),
    path('incidents/delete/<int:pk>', views_disciplinary.IncidentDeleteView.as_view(), name='incident_delete'),
    path('incidents/edit/<int:pk>', views_disciplinary.IncidentUpdateView.as_view(), name='incident_edit'),

    path('profiles/', views_profile.ProfileView.as_view(), name='profile_list'),
    path('profiles/new', views_profile.ProfileCreateView.as_view(), name='profile_new'),
    path('profiles/delete/<int:pk>', views_profile.ProfileDeleteView.as_view(), name='profile_delete'),
    path('profiles/edit/<int:pk>', views_profile.ProfileUpdateView.as_view(), name='profile_edit'),
]
