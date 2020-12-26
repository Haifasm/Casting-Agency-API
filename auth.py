from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import json
import os

from dotenv import load_dotenv
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_SIGNING_ALGORITHM = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    # "Authorization" not in header
    if not auth:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'No Authorization in Header.'
            }, 401)

    parts = auth.split()
    # "Bearer" not in "Authorization"
    if parts[0].lower() != 'bearer':
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'No Bearer in Authorization.'
            }, 401)

    elif len(parts) != 2:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Iinvalid Header.'
            }, 401)

    return parts[1]


def check_permissions(permission, payload):
    # Raise an AuthError if permissions are not included in the payload
    if 'permissions' not in payload:
        raise AuthError(
            {
                'code': 'invalid_claims',
                'description': 'Permissions not included in JWT.'
            }, 400)
    # Raise an AuthError if the requested permission string is not in the
    # payload permissions array
    if permission not in payload['permissions']:
        raise AuthError(
            {
                'code': 'Unauthorized',
                'description': 'Permission not found.'
            }, 401)
    return True


def verify_decode_jwt(token):
    # Public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # Data
    unverified_header = jwt.get_unverified_header(token)
    # Choose key
    if 'kid' not in unverified_header:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:

            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=AUTH0_SIGNING_ALGORITHM,
                                 audience=API_AUDIENCE,
                                 issuer='https://' + AUTH0_DOMAIN + '/')
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims.'
                    'Please, check the audience and issuer.'
                }, 401)

        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)

    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except BaseException:
                raise AuthError(
                    {
                        'code': 'Unauthorized',
                        'description': 'User doesn\'t have permissions.'
                    }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
