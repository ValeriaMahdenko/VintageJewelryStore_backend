import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(value):
    if re.search(r"[^A-Za-z ,.'-]+", value) is not None:
        raise ValidationError(
            _('Enter a valid data. Must contain only letters and spaces.'),
        )


def validate_price(value):
    if value <= 0:
        raise ValidationError(
            _('Enter a valid price.'))
