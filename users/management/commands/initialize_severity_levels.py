from django.core.management.base import BaseCommand
from users.models import SeverityLevel

class Command(BaseCommand):
    help = 'Initialize severity levels for the disciplinary system'

    def handle(self, *args, **kwargs):
        # Check if severity levels already exist to prevent duplicates
        existing_levels = SeverityLevel.objects.all()
        
        if existing_levels.exists():
            self.stdout.write(self.style.WARNING('Severity levels already exist. Skipping initialization.'))
            return

        # Create severity levels
        severity_levels = [
            {'level_description': 'MINOR'},
            {'level_description': 'MODERATE'},
            {'level_description': 'SEVERE'}
        ]

        for level in severity_levels:
            SeverityLevel.objects.create(**level)
            self.stdout.write(self.style.SUCCESS(f'Created severity level: {level["level_description"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully initialized severity levels'))
