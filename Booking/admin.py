from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Amenity)
admin.site.register(Venues)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Professional)
admin.site.register(ProfessionalReview)