from django import forms

from .models import Animal, VaccinationRecord


class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal

        fields = [
            'animal_id',
            'animal_type',
            'breed',
            'age',
            'gender',
            'vaccination_status',
        ]

        widgets = {
            'animal_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: COW001'
                }
            ),

            'animal_type': forms.HiddenInput(),

            'breed': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Gir, Murrah, Jamunapari'
                }
            ),

            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Age in years',
                    'min': '0'
                }
            ),

            'gender': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'vaccination_status': forms.CheckboxInput(
                attrs={
                    'class': 'vaccination-checkbox'
                }
            ),
        }

        labels = {
            'animal_id': 'Animal ID',
            'animal_type': 'Animal Type',
            'breed': 'Breed',
            'age': 'Age',
            'gender': 'Gender',
            'vaccination_status': 'Vaccination Status',
        }


class VaccinationRecordForm(forms.ModelForm):

    class Meta:
        model = VaccinationRecord

        fields = [
            'vaccine_name',
            'date_given',
            'next_due_date',
            'veterinarian_name',
            'notes',
        ]

        widgets = {

            'vaccine_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: FMD Vaccine'
                }
            ),

            'date_given': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'next_due_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'veterinarian_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Veterinarian name'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional notes'
                }
            ),
        }

        labels = {
            'vaccine_name': 'Vaccine Name',
            'date_given': 'Date Given',
            'next_due_date': 'Next Due Date',
            'veterinarian_name': 'Veterinarian Name',
            'notes': 'Notes',
        }