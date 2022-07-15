# THIS MODULE IS FOR TOKEN GENERATOR

# MODULE NEEDED TO GENERATE UNIQUE LINK FOR EMAIL CONFIRMATION
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator): #INHERITING THE CLASS FROM PASSWORD RESET TOKEN GENERATOR
    def _make_has_value(self,user,timestamp):
        return (
            text_type(user.pk) + text_type(timestamp)
        )

generate_token = TokenGenerator()