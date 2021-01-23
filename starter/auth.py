import json
import os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

#AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
#ALGORITHMS = os.environ.get('ALGORITHMS')
#API_AUDIENCE = os.environ.get('API_AUDIENCE')

AUTH0_DOMAIN = 'casting-agency-fsnd-ud.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'auth'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if "Authorization" in request.headers:
        auth_header = request.headers.get("Authorization")
        auth_header = auth_header.split(' ')
        # check first if the header contains two parts: bearer and token
        if len(auth_header) != 2:
            raise AuthError({"message": "aut header is malformed"},
                            401)
        # if the first part is not bearer
        elif auth_header[0].lower() != "bearer":
            raise AuthError({"message": "auth header has no bearer part"},
                            401)
        # if the second part doesn't contain the token
        elif not auth_header[1]:
            raise AuthError({"message": "auth header has no token part"},
                            401)
        # if the token exists it will be returned
        else:
            token = auth_header[1]
            return token
    else:
        raise AuthError({
            'message': 'Authorization header is expected.'
        }, 401)

def check_permissions(permission, payload):
    """
    This function checks if authorization permissions
    are included in the payload
    """

    if 'permissions' not in payload:
        raise AuthError({'message': 'perms are not included in the payload12'},
                        401)
    elif permission not in payload['permissions']:
        raise AuthError({'message': 'perms are not included in the payload'},
                        401)
    else:
        return True


def verify_decode_jwt(token):
   
    jsonurl = urlopen(f'http://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    header = jwt.get_unverified_header(token)

    # check if kid in header
    if 'kid' in header:
        if header['kid']:

            rsa_key = {}
            for key in jwks['keys']:
                # if  kid in jwks matches the rsa key will be created
                if key['kid'] == header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']}

            if rsa_key:
                try:
                    # create the payload
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer='https://' + AUTH0_DOMAIN + '/'
                    )
                    return payload

                
                except jwt.JWTClaimsError:
                    raise AuthError({
                        'code': 'the claims are invalid',
                        'description': 'please check the audience and issuer.'
                    }, 401)

                # exception if the token expired
                except jwt.ExpiredSignatureError:
                    raise AuthError({'code': 'token has expired',
                                     'description': 'token expired'}, 401)

                # exception in case of any error
                except Exception:
                    raise AuthError({
                        'code': 'invalid_header',
                        'description': 'Unable to parse authentication token.'
                    }, 400)
        else:
            raise AuthError({'code': 'invalid_header',
                             'description': 'Authorization malformed'}, 401)

    else:
        raise AuthError({'code': 'invalid_header',
                         'description': 'Unable to find the ke1722'},
                        400)


def requires_auth(permission=''):
    """
    This function return the decorator
    which passes the decoded payload to the decorated method
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
