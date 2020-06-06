# Alexander Shein 03.20
from rest_framework import authentication, exceptions



class BaseTokenAuthentication(authentication.BaseAuthentication):
    '''
    This is a base class intended to authentificate user by an auth_token request GET/POST parameter
    '''
    def _check_token(self, token):
        """
        This function should return either User or AnonymosUser
        and raise AuthenticationFailed if authentication was not successful
        """
        raise NotImplementedError('You should override _check_token method in order to use this Auth class')

    def authenticate(self, request):
        token = request.GET.get('auth_token') or request.POST.get('auth_token')
        if not token:
            raise exceptions.AuthenticationFailed('Authorization token was not provided')
        user = self._check_token(token)
        return (user, None)

