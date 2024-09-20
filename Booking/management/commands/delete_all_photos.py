import os
from django.core.management.base import BaseCommand
from Booking.models import Venue, Professional  # Replace with your app name

class Command(BaseCommand):
    help = 'Delete all photos from Venues and Professionals'

    def handle(self, *args, **kwargs):
        # Delete photos from Venues
        venues = Venue.objects.all()
        for venue in venues:
            if venue.image:
                venue.image.delete(save=False)
                self.stdout.write(self.style.SUCCESS(f'Deleted photo from Venue: {venue.venue_name}'))

        # Delete photos from Professionals
        professionals = Professional.objects.all()
        for professional in professionals:
            if professional.image:
                professional.image.delete(save=False)
                self.stdout.write(self.style.SUCCESS(f'Deleted photo from Professional: {professional.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully deleted all photos from Venues and Professionals'))
