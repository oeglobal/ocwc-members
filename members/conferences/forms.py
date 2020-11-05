from django import forms

from conferences.models import ConferenceEmailRegistration


class ConnectForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]

        if not ConferenceEmailRegistration.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Unknown email. Please contact conference@oeglobal.org for assistance."
            )

        return cleaned_data
