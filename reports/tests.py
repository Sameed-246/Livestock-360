from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from animals.models import Animal
from reports.models import DiseaseReport
from reports.forms import DiseaseReportForm
from ai_engine.predictor import predict_health_risk, calculate_risk_score


class HealthReportWorkflowTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='farmer_test',
            password='testpassword123'
        )
        self.animal = Animal.objects.create(
            animal_id='COW-TEST-001',
            owner=self.user,
            animal_type='Cattle',
            breed='Gir',
            age=4,
            gender='Female',
            vaccination_status=True
        )

    def test_form_location_address_fallback(self):
        """Form provides graceful location fallback if no address or coordinates given."""
        form = DiseaseReportForm(
            data={
                'animal': self.animal.id,
                'symptoms': 'Loss of appetite, coughing',
                'temperature': '39.2',
                'latitude': '',
                'longitude': '',
                'location_address': '',
            },
            user=self.user
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data['location_address'],
            'Location unavailable — veterinarian can review manually.'
        )

    def test_form_temperature_validation(self):
        """Temperature must be within realistic livestock limits."""
        form = DiseaseReportForm(
            data={
                'animal': self.animal.id,
                'symptoms': 'High fever',
                'temperature': '65.0',
            },
            user=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn('temperature', form.errors)

    def test_predictor_returns_valid_structure(self):
        """AI predictor must always return expected keys without crashing."""
        ai_data = {
            'animal_type': 'Cattle',
            'age': 4,
            'gender': 'Female',
            'vaccination_status': True,
            'symptoms': 'coughing, fever',
            'temperature': 40.2,
        }
        result = predict_health_risk(ai_data)
        self.assertIn('risk_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('predicted_disease', result)
        self.assertIn('disease_confidence', result)
        self.assertIn('recommendation', result)

    def test_report_status_transition(self):
        """Report can transition from Pending to Reviewed to Resolved."""
        report = DiseaseReport.objects.create(
            animal=self.animal,
            symptoms='Fever',
            temperature=Decimal('39.5'),
            status='Pending'
        )
        self.assertEqual(report.status, 'Pending')

        report.status = 'Reviewed'
        report.save()
        report.refresh_from_db()
        self.assertEqual(report.status, 'Reviewed')

        report.status = 'Resolved'
        report.save()
        report.refresh_from_db()
        self.assertEqual(report.status, 'Resolved')

