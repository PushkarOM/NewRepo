from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .search_logic import search_venues, search_professionals
from django.core.paginator import Paginator


#below i have created the search login for search page and booking page
def bookingpage(request):
    search_results = search_venues(request)
    if search_results is not None:
        return render(request, 'Booking/bookingpage.html', {'venues': search_results})
    else:
        venues = Venues.objects.all()
    # Implement pagination
    paginator = Paginator(venues, 21)  # Show 20 venues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'venues': page_obj,
    }
    return render(request, 'Booking/bookingpage.html', context)    
    

def search_page(request):
    search_results = search_venues(request)
    if search_results is not None:
        return render(request, 'Booking/bookingpage.html', {'venues': search_results})
        
    else:
        return render(request , 'Booking/searchpage.html')
    



#below i have created the booking form funciton this grabs the data from the form and created a booking in database.
def bookingform(request,venue_id=0):
    if request.method == "POST":
        #additionally this handels the updation of incomplete forms
        booking_ids = request.POST.getlist('booking_id')
        incomplete_bookings = Booking.objects.filter(id__in=booking_ids)
        if booking_ids :
            for booking in incomplete_bookings:
                if booking.venue :
                    # Extract details from the form
                    start_date = request.POST[f"start_date_{booking.id}"]
                    end_date = request.POST[f"end_date_{booking.id}"]
                    num_people = int(request.POST[f"num_people_{booking.id}"])
                    event_type = request.POST[f"event_type_{booking.id}"]
                    food_type = request.POST[f"food_type_{booking.id}"]
                    decoration_needed = request.POST[f"decoration_needed_{booking.id}"].lower() == "yes"
                    time_duration = request.POST[f"time_duration_{booking.id}"]
                    additional_services = request.POST[f"additional_services_{booking.id}"]

                    # Update the attributes of the booking object
                    booking.start_date = start_date
                    booking.end_date = end_date
                    booking.num_people = num_people
                    booking.event_type = event_type
                    booking.food_type = food_type
                    booking.decoration_needed = decoration_needed
                    booking.time_duration = time_duration
                    booking.additional_services = additional_services

                    # Grabbing the user & the venue
                    user = request.user
                    venue = get_object_or_404(Venues, pk=venue_id)

                    start_date_cpy = datetime.strptime(start_date, "%Y-%m-%d")
                    end_date_cpy = datetime.strptime(end_date, "%Y-%m-%d")

                    # Calculate the duration in days
                    duration_days = (end_date_cpy - start_date_cpy).days

                    # Calculate the total price
                    total_price = venue.calculate_price(num_guests=num_people, event_type=event_type, duration=duration_days)
                    
                    # Update the total price of the booking
                    booking.total_price = total_price

                    # Save the updated booking object
                    booking.save()
                    
                
                elif booking.professional :
                    # Extract details from the form
                    start_date = request.POST[f"start_date_{booking.id}"]
                    end_date = request.POST[f"end_date_{booking.id}"]
                    event_type = request.POST[f"event_type_{booking.id}"]
                    

                    # Update the attributes of the booking object
                    booking.start_date = start_date
                    booking.end_date = end_date
                    booking.num_people = 1
                    booking.event_type = event_type
                    booking.food_type = "NOTHING"
                    booking.decoration_needed = False
                    
                    booking.additional_services = "NOTHING"

                    # Grabbing the user
                    user = request.user
                    

                    start_date_cpy = datetime.strptime(start_date, "%Y-%m-%d")
                    end_date_cpy = datetime.strptime(end_date, "%Y-%m-%d")

                    # Calculate the duration in days
                    duration_days = (end_date_cpy - start_date_cpy).days
                    booking.time_duration = duration_days
                    # Calculate the total price
                    total_price = duration_days*24*(booking.professional.price_range)
                    
                    # Update the total price of the booking
                    booking.total_price = total_price

                    # Save the updated booking object
                    booking.save()
            booking = Booking.objects.filter(user = user)
            return render(request, 'Booking/cartpage.html', {'bookings':booking})
        else:
        
            # Extracting the details of the booking from the Form
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]

            #converting the num_people form str to int
            num_people = request.POST["num_people"]
            num_people = int(num_people)
            
            event_type = request.POST["event_type"]
            food_type = request.POST["food_type"]
            decoration_needed = request.POST["decoration_needed"]
            time_duration = request.POST["time_duration"]
            additional_services = request.POST["additional_services"]

            #As decoration need is a boolean feild
            if decoration_needed.lower() == "yes":
                decoration_needed = True
            else:
                decoration_needed = False
            
            # Grabbing the user & the venue
            user = request.user
            venue = get_object_or_404(Venues, pk=venue_id)

            start_date_cpy = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_cpy = datetime.strptime(end_date, "%Y-%m-%d")

            # Calculate the duration in days
            duration_days = (end_date_cpy - start_date_cpy).days

            # Calling the funtion in the Venues model for calculation the price.
            total_price = venue.calculate_price(num_guests= num_people,event_type= event_type,duration=duration_days)


            # Create and save a new Booking object
            booking = Booking.objects.create(
                start_date=start_date,
                end_date=end_date,
                num_people=num_people,
                event_type=event_type,
                food_type=food_type,
                decoration_needed=decoration_needed,
                time_duration=time_duration,
                additional_services=additional_services,
                user=user, 
                venue=venue,
                total_price = total_price,
                payment_status = "UNDECIDED",
            )
            return redirect('mainpage:mainpage') #this will actually be redirected to payment page.
        
        
    else:   
    
        context = get_object_or_404(Venues,pk=venue_id) 
        return render(request, 'Booking/bookingform.html',{'venue':context})
        

#Below function loads up the page for a specific venue that is being clicked on
def venuepage(request,venue_id):
    venue = get_object_or_404(Venues,pk=venue_id)
    bookings = Booking.objects.filter(venue_id = venue_id)
    reviews = Review.objects.filter(venue_id=venue_id)
    if bookings == None :
        bookings = []
        return render(request,'Booking/venuepage.html',{'venue':venue,'bookings':bookings,'reviews':reviews})
    else:    
        return render(request,'Booking/venuepage.html',{'venue':venue,'bookings':bookings,'reviews':reviews})



#The below function adds the Venue to be Booked without any details with just user and what venue
#other details can be taken care of at the Cartpage
def bookinglistadder(request,venue_id):
    user = request.user
    venue = get_object_or_404(Venues, pk=venue_id)
    
    booking = Booking.objects.create(
            user=user, 
            venue=venue,
            payment_status = "UNDECIDED",
    )
    venues = Venues.objects.all()
    paginator = Paginator(venues, 21)  # Show 20 venues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'venues': page_obj,
    }
    return render(request, 'Booking/bookingpage.html', context)





#Below function loads up the cart page
def cartpage(request):
    #creating seprate html page for authenticated and not authenticated user
    if request.user.is_authenticated:
        user = request.user
        booking = Booking.objects.filter(user = user, booking_status = False)
        return render(request, 'Booking/cartpage.html', {'bookings':booking})
    else :
        booking = []
        return render(request, 'Booking/cartpage.html', {'bookings':booking})
    


#below function is for search suggestion when a person types in search bar
def search_suggestions(request):
    query = request.GET.get('query', '')

    if query:
        # Get suggestions from Venues
        venue_suggestions = list(Venues.objects.filter(
            Q(venue_name__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        )[:10])

        suggestions = venue_suggestions 
        data = [{'name': suggestion.venue_name }for suggestion in suggestions]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def search_suggestions_prof(request):
    query = request.GET.get('query', '')
    if query:
        # Get suggestions from Professional
        suggestions = list(Professional.objects.filter(
            Q(profession__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(name__icontains=query)
        )[:10])
        
        data = [{'name': suggestion.name }for suggestion in suggestions]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


#This funtion confirms that all the feild in all the user's bookings are filled
def checkout_verification(request):
    booking_ids = request.POST.getlist('booking_ids')
    bookings = Booking.objects.filter(id__in=booking_ids)
    if request.method == 'POST':
    
        # Validate that all required fields are filled
        incomplete_bookings = []
        incomplete_booking_ids = []
        for booking in bookings:
            

            if (
                not booking.start_date or
                not booking.end_date or
                not booking.num_people or
                not booking.food_type or
                not booking.event_type or
                not booking.time_duration
            ):
                incomplete_bookings.append(booking)
                incomplete_booking_ids.append(booking.id)

        if incomplete_bookings:
                return render(request,'Booking/bookingform.html',{"incomplete_bookings":incomplete_bookings})
            
        total_price = sum(booking.total_price for booking in bookings)
        return render(request, 'Payment/checkout.html', {'bookings': bookings, 'booking_ids':booking_ids,'total_price': total_price})
    else:
        return render(request,'Booking/cartpage.html',{'bookings':bookings}) 
    




def booking_professional_page(request):
    search_results = search_professionals(request)
    if search_results is not None:
        return render(request, 'Booking/bookingpage_professional.html', {'page_obj': search_results})
    else:
        professional = Professional.objects.all()
    # Implement pagination
    paginator = Paginator(professional, 21)  # Show 20 professionals per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Booking/bookingpage_professional.html', context)


def professional_page(request,professional_id):
    professional = get_object_or_404(Professional,pk=professional_id)
    bookings = Booking.objects.filter(professional_id = professional_id)
    reviews = ProfessionalReview.objects.filter(professional_id = professional_id)
    if bookings == None :
        bookings = []
        return render(request,'Booking/professionalspage.html',{'professional':professional,'bookings':bookings,'reviews':reviews})
    else:    
        return render(request,'Booking/professionalspage.html',{'professional':professional,'bookings':bookings,'reviews':reviews})
    



#below i have created the booking form funciton this grabs the data from the form and created a booking in database.
def professionalsbookingform(request,professional_id):
    if request.method == "POST":

        start_date = request.POST[f"start_date"]
        end_date = request.POST[f"end_date"]
        event_type = request.POST[f"event_type"]

        # Grabbing the user & the professional
        user = request.user
        professional = get_object_or_404(Professional, pk=professional_id)

        start_date_cpy = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_cpy = datetime.strptime(end_date, "%Y-%m-%d")

        # Calculate the duration in days
        duration_days = (end_date_cpy - start_date_cpy).days

        # Calling the funtion in the Venues model for calculation the price.
        total_price = duration_days*24*(professional.price_range)


        # Create and save a new Booking object
        booking = Booking.objects.create(
            start_date=start_date,
            end_date=end_date,
            num_people=0,
            event_type=event_type,
            food_type="FALSE",
            decoration_needed=False,
            time_duration=duration_days,
            additional_services="FALSE",
            user=user, 
            professional=professional,
            total_price = total_price,
            payment_status = "UNDECIDED",
        )
        return redirect('Booking:cartpage') #this will actually be redirected to payment page.

    else:   
        professional = get_object_or_404(Professional, pk=professional_id)
        return render(request, 'Booking/professionalsbooking_form.html',{'professional':professional})
    


def professionalsbookinglistadder(request,professional_id):
    user = request.user
    professional = get_object_or_404(Professional, pk=professional_id)
    
    booking = Booking.objects.create(
            user=user, 
            professional=professional,
            payment_status = "UNDECIDED",
    )
    professional = Professional.objects.all()
    # Implement pagination
    paginator = Paginator(professional, 21)  # Show 20 professionals per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'Booking/bookingpage_professional.html', context)