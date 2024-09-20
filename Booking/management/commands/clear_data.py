from django.core.management.base import BaseCommand
from Booking.models import Venues, Professional, Review, ProfessionalReview, Amenity,Booking

class Command(BaseCommand):
    help = 'Clear all data from the database'

    def handle(self, *args, **kwargs):
        Review.objects.all().delete()
        ProfessionalReview.objects.all().delete()
        Venues.objects.all().delete()
        Professional.objects.all().delete()
        Booking.objects.all().delete()
        Amenity.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data'))
