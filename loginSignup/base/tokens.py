from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

#this is a token generator class that will generate a token for the user to verify their email
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.email_is_verified)
        )
account_activation_token = TokenGenerator()
