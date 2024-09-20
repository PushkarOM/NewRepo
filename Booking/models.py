from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Below i have created a Feild that takes all the amenities provided by the venue (parking,wifi) <--this format
class Amenity(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

#Below i have created the Venues Model that takes in most of the neccessary information of a venue
class Venues(models.Model):
    venue_name = models.CharField(max_length=200, null=True)
    base_price = models.FloatField()  # Base price for a Venue 
    #locaiton of venue
    state = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    
    #details about the venue
    seating_capacity = models.IntegerField()
    description = models.TextField(null=True)
    amenities = models.ManyToManyField(Amenity)
    rating = models.FloatField(null=True, blank=True)

    #Contact Details
    contact_number = models.CharField(max_length=15, null=True)
    contact_email = models.EmailField(null=True)
    image = models.ImageField(upload_to='venue_images/', null=True, blank=True)
    
    def booked_dates(self):
        # Retrieve all booked dates for the venue
        today = timezone.now().date()
        return Booking.objects.filter(venue=self, date__gte=today).values_list('date', flat=True)

    #funciton to calculate the total price after the user fills a form    
    def calculate_price(self, num_guests, event_type, duration): #the arguments may change
        price = self.base_price
        if event_type == 'wedding':
            price += 500  # Additional cost for weddings
        if num_guests > 100:
            price += 10 * (num_guests - 100)  # Extra charge per guest over a base value say 100
        price *= duration  # Multiply by number of days
        return price

    def __str__(self):
        return self.venue_name


#Below i have created a Review Model this will store the review about the venue and rating given by the customer
class Review(models.Model):
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  
    rating = models.IntegerField()
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.venue.venue_name} by {self.user.username}'
    
class Professional(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=255,blank=True)
    state = models.CharField(max_length=255,blank=True)
    profession = models.CharField(max_length=255)
    price_range = models.DecimalField(max_digits=10, decimal_places=2)
    portfolio = models.URLField()
    availability = models.BooleanField()
    contact_email = models.CharField(max_length=255,blank=True)
    contact_number = models.IntegerField(blank=True,default= 0)
    image = models.ImageField(upload_to='prof_images/', null=True, blank=True)
    def __str__(self):
        return self.name

class ProfessionalReview(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_posted = models.DateField()

    def __str__(self):
        return f'Review for {self.professional.name} by {self.user.username}'
    


#Below i have created the booking model that keep all the details about the booking for a particular venue done by the user
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE,null=True,blank=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE,null=True,blank=True)
    
    #Feilds to be filled by user and shown to them
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    num_people = models.IntegerField(blank=True, null=True)
    food_type = models.CharField(max_length=100,blank=True, null=True)
    event_type = models.CharField(max_length=100,blank=True, null=True)
    decoration_needed = models.BooleanField(default=False)
    time_duration = models.CharField(max_length=100, blank=True, null=True)
    additional_services = models.TextField(blank=True)
    
    #Feilds to be only shown to the users
    total_price = models.DecimalField(max_digits=1000, decimal_places=2,blank=True, null=True)
    payment_status = models.CharField(max_length=50)
    booking_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.start_date} to {self.end_date}'
    


