from django.db.models import EmailField, CharField

class LowerCaseEmailField(EmailField):
    def to_python(self, value: str):
        value = super().to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value

class LowerCaseCharField(CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value
