"""Web socket middleware for token authentication"""

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings

User = get_user_model()

@database_sync_to_async
def get_user(validated_token):
    """
    Retrieves a user instance based on the user ID in the validated token. 
    If the user does not exist, returns an AnonymousUser instance.

    Parameters:
    validated_token: Dict
        A dictionary containing a validated token. 
        The token should include a "user_id" key.

    Returns:
        User: A user instance if the user exists. Otherwise, an AnonymousUser 
        instance.
    """
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user
   
    except User.DoesNotExist:
        return AnonymousUser()



class JwtAuthMiddleware(BaseMiddleware):
    """
    Middleware for JWT Authentication. It validates the JWT token from the query string 
    and attaches the user to the scope if the token is valid.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        Validate JWT token, and attach user to the scope.
        """
       # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # Get the user and add it to the scope, so that
            # we can access it in the consumer
            scope["user"] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))