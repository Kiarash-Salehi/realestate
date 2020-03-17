from django.shortcuts import render
from listings.models import Listings
from realtors.models import Realtor
from listings.choices import price_choices, bedroom_choices, state_choices


# Create your views here.

def index(request):
    listings = Listings.objects.order_by('-list_date').filter(is_published=True)[:3]

    context = {
        'listings': listings,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
    }
    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.order_by('-hire_date')
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors,
        }
    return render(request, 'pages/about.html', context)