from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'email', 'telephone', 'nombre_places']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@email.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '243XXXXXXXXX'}),
            'nombre_places': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10, 'value': 1}),
        }