from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import BuildingManagerToken

class BuildingManagerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token_key = request.headers.get('Authorization')
        print(token_key)
        if not token_key:
            return None

        if token_key.startswith('Token '):
            token_key = token_key.split(' ')[1]
        
        try:
            token = BuildingManagerToken.objects.get(key=token_key)
        except BuildingManagerToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)
