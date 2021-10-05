from .models import ShopUser
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class ShopUserForm(forms.ModelForm):
    # set the label name of the date field.
    email = forms.EmailField(max_length=180)
    phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': ('Phone')}), label=("Phone number"),
        required=False)

    class Meta:
        model = ShopUser
        fields = ("__all__")
        exclude = ['is_admin', 'is_superuser', 'is_active', 'last_login']
