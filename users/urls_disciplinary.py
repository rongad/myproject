from django.urls import path
from . import views_disciplinary

urlpatterns = [
    path('incidents/', views_disciplinary.incident_list, name='incident_list'),
    path('incidents/report/', views_disciplinary.report_incident, name='report_incident'),
    path('incidents/<int:incident_id>/', views_disciplinary.incident_detail, name='incident_detail'),
    path('incidents/<int:incident_id>/sanction/', views_disciplinary.issue_sanction, name='issue_sanction'),
    path('sanctions/<int:sanction_id>/approve/', views_disciplinary.approve_sanction, name='approve_sanction'),
    path('students/<str:student_id>/history/', views_disciplinary.student_history, name='student_history'),
]
