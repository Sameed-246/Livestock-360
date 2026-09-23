from django import forms
from decimal import Decimal, InvalidOperation

from .models import DiseaseReport
from animals.models import Animal


class DiseaseReportForm(forms.ModelForm):

    # Receive GPS values as text first.
    # This prevents Django from rejecting long GPS decimals
    # before our cleaning code runs.
    latitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    longitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = DiseaseReport

        fields = [
            'animal',
            'symptoms',
            'temperature',
            'image',
            'latitude',
            'longitude',
            'location_address',
        ]

        widgets = {

            'animal': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'symptoms': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': (
                        'Example: fever, not eating, coughing...'
                    )
                }
            ),

            'temperature': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 40.5',
                    'step': '0.1'
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*',
                    'capture': 'environment'
                }
            ),

            'location_address': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:

            self.fields['animal'].queryset = (
                Animal.objects
                .filter(owner=user)
                .order_by('-created_at')
            )

        else:

            self.fields['animal'].queryset = (
                Animal.objects.none()
            )

    def clean_latitude(self):

        value = self.cleaned_data.get('latitude')

        if not value:
            return None

        try:
            number = Decimal(str(value))

            # Keep only 7 decimal places
            return number.quantize(
                Decimal('0.0000001')
            )

        except (InvalidOperation, ValueError):

            return None

    def clean_longitude(self):

        value = self.cleaned_data.get('longitude')

        if not value:
            return None

        try:
            number = Decimal(str(value))

            # Keep only 7 decimal places
            return number.quantize(
                Decimal('0.0000001')
            )

        except (InvalidOperation, ValueError):

            return None