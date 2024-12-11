from django.urls import path
from django.contrib.auth import views as auth_views

from users import views_disciplinary
from . import views



urlpatterns = [
    path('', views.login_view, name='login'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('view_transaction/', views.view_transaction, name='view_transaction'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),

    path('incidents/', views_disciplinary.IncidentView.as_view(), name='incident_list'),
    path('incidents/new', views_disciplinary.IncidentCreateView.as_view(), name='incident_new'),
    path('incidents/delete/<int:pk>', views_disciplinary.IncidentDeleteView.as_view(), name='incident_delete'),
    path('incidents/edit/<int:pk>', views_disciplinary.IncidentUpdateView.as_view(), name='incident_edit'),
]
