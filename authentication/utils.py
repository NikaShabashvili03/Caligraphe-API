import jwt
import requests
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, DecodeError

def verify_google_token(id_token):
    """
    Verifies the Google OAuth token and returns the decoded token if valid.
    """
    try:
        # Decode the token header to get the key ID (kid)
        unverified_header = jwt.get_unverified_header(id_token)
        if unverified_header is None:
            raise DecodeError("Invalid token")

        # Fetch the public keys from Google's OAuth2 endpoint
        response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
        certs = response.json()

        # Find the key corresponding to the 'kid' in the token header
        rsa_key = {}
        for cert in certs["keys"]:
            if cert["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": cert["kty"],
                    "kid": cert["kid"],
                    "use": cert["use"],
                    "n": cert["n"],
                    "e": cert["e"],
                }
                break

        if not rsa_key:
            raise DecodeError("Unable to find appropriate key")

        # Decode and verify the JWT using the public key
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)
        decoded_token = jwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"],
            audience=settings.GOOGLE_CLIENT_ID,  # Use your Google OAuth client ID as the audience
        )

        return decoded_token

    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token has expired")
    except DecodeError:
        raise DecodeError("Invalid token")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Error fetching Google's public keys: {str(e)}")
    

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip