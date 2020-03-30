from django import forms

class FlightForm(forms.Form):
    places = forms.CharField(label='flight stops', max_length=200)
    flight_class = forms.CharField(label='flight class', max_length=20)