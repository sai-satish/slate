from django import forms
from authentication.models import User

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]  # Add more fields if needed

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
