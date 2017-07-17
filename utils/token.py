from itsdangerous import URLSafeTimedSerializer
import base64
from django.conf import settings


# producing token and get token when users confirm from email to authenticate.
class Token(object):
    def __init__(self,security_key=settings.SECRET_KEY,salt=settings.SALT):
        self.security_key=security_key
        self.salt=salt

    # generate token from email/username/id etc.
    def generate_confirmation_token(self,code):
        serializer=URLSafeTimedSerializer(self.security_key)
        return serializer.dumps(code,salt=self.salt)

    # de serialize token if there expiration is not expired.
    def confirm_token(self, token, expiration=3600):
        serializer=URLSafeTimedSerializer(self.security_key)
        try:
            code=serializer.loads(token,salt=self.salt,max_age=expiration)
        except:
            return False
        return code
