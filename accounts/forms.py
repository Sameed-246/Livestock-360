from django import forms
from django.contrib.auth.models import User


class FarmerRegistrationForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create your password",
                "autocomplete": "new-password",
            }
        ),
        required=True,
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password again",
                "autocomplete": "new-password",
            }
        ),
        required=True,
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1:
            self.add_error(
                "password1",
                "Please enter a password."
            )

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "Passwords do not match."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Securely hash the farmer's chosen password.
        user.set_password(
            self.cleaned_data["password1"]
        )

        if commit:
            user.save()

        return user