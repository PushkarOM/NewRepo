import os
import random
from django.core.management.base import BaseCommand
from Booking.models import Professional  # Replace with your app name
from PIL import Image
from django.core.files import File

class Command(BaseCommand):
    help = 'Randomly upload images to professionals based on their profession'

    def handle(self, *args, **kwargs):
        image_folder = 'D:\\CodeStuff\\Ayojan\\Mock_images_prof'  # Folder where the images are stored
        images = os.listdir(image_folder)  # List all image files in the folder
        professionals = Professional.objects.all()

        # Separate images into two categories
        venue_images = [img for img in images if 'venue' in img]
        photo_images = [img for img in images if 'photo' in img]

        for professional in professionals:
            if professional.profession == 'Decorator':
                if not venue_images:
                    self.stdout.write(self.style.ERROR('No venue images available.'))
                    continue
                random_image = random.choice(venue_images)
            else:
                if not photo_images:
                    self.stdout.write(self.style.ERROR('No photo images available.'))
                    continue
                random_image = random.choice(photo_images)

            image_path = os.path.join(image_folder, random_image)

            # Create a new image name based on the professional name
            new_image_name = f'{professional.name}_{professional.profession}{os.path.splitext(random_image)[1]}'

            # Open the image using Pillow and assign it to the professional
            with open(image_path, 'rb') as img_file:
                professional.image.save(new_image_name, File(img_file), save=True)

            self.stdout.write(self.style.SUCCESS(f'Uploaded {new_image_name} to {professional.name}'))
