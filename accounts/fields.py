from django.db.models import EmailField, CharField

# Custom Email field for converting email to lowercase
class LowerCaseEmailField(EmailField):
    def to_python(self, value: str):
        value = super().to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value

# Custom Char field.
class LowerCaseCharField(CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value
