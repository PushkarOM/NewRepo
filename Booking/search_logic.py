from django.db.models import Q
from .models import *
from django.core.paginator import Paginator

def search_venues(request):
    if 'search' in request.GET or 'baseprice' in request.GET:
        search_query = request.GET.get('search', '')
        base_price = request.GET.get('baseprice', '')
        city = request.GET.get('city', '')
        state = request.GET.get('state', '')

        filters = Q()
        
        if search_query:
            filters &= (
                Q(venue_name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(state__icontains=search_query)
            )

        if city:
            filters &= Q(city__icontains=city)

        if state:
            filters &= Q(state__icontains=state)

        if base_price:
            try:
                base_price = float(base_price)
                filters &= Q(base_price__lte=base_price)
            except ValueError:
                pass
        
        search_results = Venues.objects.filter(filters)
        return search_results
    
def search_professionals(request):
    if 'search' in request.GET or 'baseprice' in request.GET:
        search_query = request.GET.get('search', '')
        base_price = request.GET.get('baseprice', '')
        city = request.GET.get('city', '')
        state = request.GET.get('state', '')


        filters = Q()
        
        if search_query:
            filters &= (
                Q(name__icontains=search_query) |
                Q(profession__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(state__icontains=search_query)
            )

        if city:
            filters &= Q(city__icontains=city)

        if state:
            filters &= Q(state__icontains=state)

        if base_price:
            try:
                base_price = float(base_price)
                filters &= Q(base_price__lte=base_price)
            except ValueError:
                pass
        
        search_results = Professional.objects.filter(filters)
        return search_results    
