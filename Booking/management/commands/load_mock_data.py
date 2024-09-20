import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Booking.models import Venues, Professional, Amenity, ProfessionalReview, Review
from django.shortcuts import get_object_or_404

class Command(BaseCommand):
    help = 'Load mock data into the database'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(__file__)

        with open(os.path.join(base_dir, 'venues.json')) as f:
            venues = json.load(f)
        
        with open(os.path.join(base_dir, 'professionals.json')) as f:
            professionals = json.load(f)

        with open(os.path.join(base_dir, 'venue_reviews.json')) as f:
            venue_reviews = json.load(f)
        
        with open(os.path.join(base_dir, 'professional_reviews.json')) as f:
            professional_reviews = json.load(f)

        # Fetch users from the database
        users = {user.username: user for user in User.objects.filter(username__in=['om', 'ompushkar', 'Khushi'])}

        # Create amenities and venues
        for venue_data in venues:
            amenities_data = venue_data.pop('amenities')
            venue = Venues.objects.create(**venue_data)
            for amenity_name in amenities_data:
                amenity, created = Amenity.objects.get_or_create(name=amenity_name)
                venue.amenities.add(amenity)
            venue.save()

        # Create professionals
        for professional_data in professionals:
            Professional.objects.create(**professional_data)

        # Create venue reviews
        for review_data in venue_reviews:
            venue = get_object_or_404(Venues, pk=int(review_data['venue_id']))
            user = users.get(review_data['user'])
            Review.objects.create(
                venue=venue,
                user=user,
                rating=review_data['rating'],
                comment=review_data['comment'],
                date_posted=review_data['date_posted']
            )

        # Create professional reviews
        for review_data in professional_reviews:
            professional = get_object_or_404(Professional, pk=int(review_data['professional_id']))
            user = users.get(review_data['user'])
            ProfessionalReview.objects.create(
                professional=professional,
                user=user,
                rating=review_data['rating'],
                comment=review_data['comment'],
                date_posted=review_data['date_posted']
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded mock data'))
