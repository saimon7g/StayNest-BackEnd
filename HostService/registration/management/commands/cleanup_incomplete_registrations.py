# myapp/management/commands/cleanup_incomplete_registrations.py
from django.core.management.base import BaseCommand
from registration.models import PropertyRegistration

class Command(BaseCommand):
    help = 'Cleanup incomplete registrations'

    def handle(self, *args, **options):
        incomplete_registrations = PropertyRegistration.objects.filter(
            step2__isnull=True
        )

        count = incomplete_registrations.count()
        self.stdout.write(f'Found {count} incomplete registrations')

        # Delete incomplete registrations
        incomplete_registrations.delete()

        self.stdout.write('Cleanup complete')
