from django.core.exceptions import ValidationError
from django.utils.translation import ungettext

class MaximumLengthValidator(object):
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ungettext(
                    "This password is too long. It must contain at most %(max_length)d character.",
                    "This password is too long. It must contain at most %(max_length)d characters.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ungettext(
            "Your password must contain at most %(max_length)d character.",
            "Your password must contain at most %(max_length)d characters.",
            self.max_length
        ) % {'max_length': self.max_length}
