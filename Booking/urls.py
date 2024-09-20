from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "Booking"


urlpatterns = [
    path("",views.bookingpage,name ='bookingpage'),
    path("search/",views.search_page,name ='search_view'),
    path("form/<int:venue_id>",views.bookingform,name="booking_form"),
    path("Venue/<int:venue_id>",views.venuepage,name="venuepage"),
    path("list/",views.cartpage,name="cartpage"),
    path("succefullyadded/<int:venue_id>",views.bookinglistadder,name="bookinglistadder"),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search-suggestions-professionals/', views.search_suggestions_prof, name='search_suggestions_prof'),
    path('checkout/',views.checkout_verification,name="checkout"),
    path('professionals/',views.booking_professional_page,name="professional"),
    path('professional/<int:professional_id>',views.professional_page,name='professionalspage'),
    path('professionalsform/<int:professional_id>',views.professionalsbookingform,name="professionalsbookingform"),
    path('succesfullyaddedprofessional/<int:professional_id>',views.professionalsbookinglistadder,name="professionalsbookinglistadder")



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)