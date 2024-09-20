import jwt
import random
import string
import requests
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.crypto import constant_time_compare


# Utility to verify and decode the JWT token
def decode_id_token(id_token):
    unverified_header = jwt.get_unverified_header(id_token)

    # Get the public keys from Okta to verify the signature
    jwks_url = f"https://{settings.OKTA_DOMAINN}/oauth2/default/v1/keys"
    jwks_response = requests.get(jwks_url)
    jwks = jwks_response.json()

    # Find the key matching the 'kid' fromt the token header
    rsa_key = {}
    for key in jwks["key"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if rsa_key:
        # Verify the token using the public key and decode the payload
        payload = jwt.decode(
            id_token,
            key=rsa_key,
            algorithms=["RS256"],
            audience=settings.OIDC_RP_CLIENT_ID,
            issuer=f"https://{settings.OKTA_DOMAIN}/oauth2/default",
        )
        return payload
    else:
        raise ValueError("Unable to find appropriate key to verify the token")


def oidc_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code or not state:
        return HttpResponseBadRequest("Missing code or state")

    if not constant_time_compare(state, request.session.get("oidc_state")):
        return HttpResponseBadRequest("Invalid state")

    token_url = f"https://{settings.OKTA_DOMAIN}/oauth2/default/v1/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": request.build_absolute_uri("/oidc/callback"),
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "client_secret": settings.OIDC_RP_CLIENT_SECRET,
    }

    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        return HttpResponseBadRequest("Failed to get tokens")

    tokens = token_response.json()
    access_token = tokens.get("access_token")
    id_token = tokens.get("id_token")

    if not id_token:
        return HttpResponseBadRequest("Missing ID token")

    try:
        id_token_payload = decode_id_token(id_token)
    except jwt.ExpiredSignatureError:
        return HttpResponseBadRequest("ID token has expired")
    except jwt.JWTClaimsError:
        return HttpResponseBadRequest("Invalid claims in ID token")
    except Exception as e:
        return HttpResponseBadRequest(f"ID token verification failed: {str(e)}")

    # Get the unique user identifier from the ID token
    user_sub = id_token_payload.get("sub")
    email = id_token_payload.get("email")

    if not user_sub:
        return HttpResponseBadRequest("Invalid ID token: missing sub")

    user, created = User.objects.get_or_create(
        username=user_sub, defaults={"email": email}
    )

    login(request, user)

    # Store tokens in session or handle them as needed
    request.session["access_token"] = access_token
    request.session["id_token"] = id_token

    return redirect("/")


def generate_state():
    return "".join(random.choice(string.ascii_letters + string.digits, k=16))
    # return hashlib.sha256(os.urandom(1024)).hexdigest()


def oidc_authentication(request):
    state = generate_state()
    request.session["oidc_state"] = state
    authorization_url = f"https://{settings.OKTA_DOMAIN}/oauth2/default/v1/authorize"
    params = {
        "response_type": "code",
        "scope": "openid profile email",
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "redirect_uri": request.build_absolute_uri("/oidc/callback/"),
        "state": state,
    }
    url = request.Request("GET", authorization_url, params=params).prepare().url
    return redirect(url)
