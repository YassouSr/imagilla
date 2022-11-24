from  django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Validate User URL
def validate_urlField(url):
        valid = URLValidator()
        try:
            valid(url)
        except ValidationError:
            return False

