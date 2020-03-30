from django.shortcuts import render
from django.http import HttpResponse
from .models import FlightInfo
from .forms import *

from src.flight import Flight
from src.converter import Converter

# Functions represent views

def index(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            places = ''.join(form.cleaned_data['places']).split(',')
            flight_class = ''.join(form.cleaned_data['flight_class'])

            flight = Flight(places=places, flight_class=flight_class)
            print(flight.flight_class)
            converter = Converter()
            tree_count = converter.emission_to_trees(flight.carbon_eq)

            response_text = 'You need to plant ' + str(tree_count) + ' trees in order to offset your emissions!'
            return HttpResponse(response_text)
    else:
        form = FlightForm()

    return render(request, 'form.html', {'form': form})