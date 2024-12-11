from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Student, DisciplinaryIncident, Sanction, SeverityLevel, Staff
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings

def is_staff_member(user):
    try:
        return hasattr(user, 'staff') and user.staff.role in ['POD', 'ADMIN']
    except Staff.DoesNotExist:
        return False

def is_admin(user):
    try:
        return hasattr(user, 'staff') and user.staff.role == 'ADMIN'
    except Staff.DoesNotExist:
        return False

@login_required
@user_passes_test(is_staff_member)
def incident_list(request):
    incidents = DisciplinaryIncident.objects.all().order_by('-date')
    return render(request, 'disciplinary/incident_list.html', {'incidents': incidents})

@login_required
@user_passes_test(is_staff_member)
def report_incident(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        description = request.POST.get('description')
        severity_level_id = request.POST.get('severity_level')
        
        try:
            student = Student.objects.get(student_id=student_id)
            severity_level = SeverityLevel.objects.get(level_id=severity_level_id)
            staff = request.user.staff

            incident = DisciplinaryIncident.objects.create(
                student=student,
                description=description,
                severity_level=severity_level,
                reported_by=staff
            )

            messages.success(request, 'Incident reported successfully.')
            return redirect('incident_detail', incident_id=incident.incident_id)
        except (Student.DoesNotExist, SeverityLevel.DoesNotExist) as e:
            messages.error(request, str(e))
    
    students = Student.objects.all()
    severity_levels = SeverityLevel.objects.all()
    return render(request, 'disciplinary/report_incident.html', {
        'students': students,
        'severity_levels': severity_levels
    })

@login_required
@user_passes_test(is_staff_member)
def issue_sanction(request, incident_id):
    incident = get_object_or_404(DisciplinaryIncident, incident_id=incident_id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        duration = int(request.POST.get('duration'))
        
        try:
            sanction = Sanction.objects.create(
                incident=incident,
                student=incident.student,
                description=description,
                duration=duration,
                severity_level=incident.severity_level,
                issued_by=request.user.staff
            )
            
            # Send email notification for moderate and severe incidents
            if incident.severity_level.level_description in ['MODERATE', 'SEVERE']:
                # Note: This is a placeholder. You'll need to add actual email functionality
                subject = f'Disciplinary Incident Report - {incident.student.name}'
                message = f'''
                Dear Parent/Guardian,
                
                This is to inform you that {incident.student.name} has been involved in a disciplinary incident.
                Severity: {incident.severity_level.level_description}
                Date: {incident.date}
                Sanction: {sanction.description} ({sanction.duration} days)
                
                Please contact the school administration for more details.
                '''
                # Uncomment and configure email settings to enable email notifications
                # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [parent_email])
            
            messages.success(request, 'Sanction issued successfully.')
            return redirect('incident_detail', incident_id=incident_id)
        except ValidationError as e:
            messages.error(request, str(e))
    
    return render(request, 'disciplinary/issue_sanction.html', {'incident': incident})

@login_required
@user_passes_test(is_admin)
def approve_sanction(request, sanction_id):
    sanction = get_object_or_404(Sanction, sanction_id=sanction_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            sanction.status = 'APPROVED'
            messages.success(request, 'Sanction approved successfully.')
        elif action == 'reject':
            sanction.status = 'CANCELLED'
            messages.success(request, 'Sanction cancelled.')
        sanction.save()
        
    return redirect('incident_detail', incident_id=sanction.incident.incident_id)

@login_required
@user_passes_test(is_staff_member)
def student_history(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    incidents = DisciplinaryIncident.objects.filter(student=student).order_by('-date')
    incident_count = incidents.count()
    severity_distribution = incidents.values('severity_level__level_description').annotate(
        count=Count('incident_id')
    )
    
    return render(request, 'disciplinary/student_history.html', {
        'student': student,
        'incidents': incidents,
        'incident_count': incident_count,
        'severity_distribution': severity_distribution
    })
