from datetime import datetime, timedelta
from typing import Set, List

from eve.auth import BasicAuth

from flask import render_template
from flask_login.utils import current_user
from flask_oauthlib.provider import OAuth2Provider
from flask_security.core import Security
from flask_security.datastore import MongoEngineUserDatastore
from flask_security.utils import verify_password, config_value
from flask_security.registerable import generate_confirmation_link, user_registered, _security
from flask_mail import Message
from mongoengine.connection import get_db

from pyor.models import Client, Token, User, Role


user_datastore = MongoEngineUserDatastore(get_db(), User, Role)
security = Security()

oauth = OAuth2Provider()

@oauth.clientgetter
def load_client(client_id:str):
    return Client.objects.get(client_id=client_id)


@oauth.tokengetter
def load_token(access_token:str=None, refresh_token:str=None):
    if access_token:
        return Token.objects.get(access_token=access_token).select_related()
    elif refresh_token:
        return Token.objects.get(refresh_token=refresh_token).select_related()


@oauth.tokensetter
def save_token(token: dict, request, *args, **kwargs):
    client = Client.objects.get(client_id=request.client.client_id)
    user = User.objects.get(id=request.user.id) if request.user else current_user._get_current_object()

    tokens = Token.objects(client=client.id, user=user.id)
    # make sure that every client has only one token connected to a user
    for t in tokens:
        t.delete()

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    return Token(
        access_token=token['access_token'],
        refresh_token=token.get('refresh_token'),
        token_type=token['token_type'],
        scopes=_filter_allowed_scopes(user, token['scope'].split(" ")),
        expires=expires,
        client=client,
        user=user,
    ).save()


@oauth.usergetter
def get_user(email, password, *args, **kwargs):
    user = user_datastore.get_user(email)

    if verify_password(password, user.password):
        return user
    return None


class BearerAuth(BasicAuth):

    def authorized(self, allowed_scopes: List[str], resource: str, method: str):
        """ Validates the the current request is allowed to pass through.
        :param allowed_scopes: allowed scopes for the current request.
        :param resource: resource being requested.
        """
        try:
            valid, req = oauth.verify_request(allowed_scopes)
            if valid:
                self.set_user_or_token(req.user)
                self.set_request_auth_value(req.user.id)
                return True
        except:
            pass
        return False

def user_registered_callback(user: User):
    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)

    user_registered.send(security.app, user=user, confirm_token=token)

    if config_value('SEND_REGISTER_EMAIL'):
        send_mail(config_value('EMAIL_SUBJECT_REGISTER'), user["email"],
                  'welcome', user=user, confirmation_link=confirmation_link)

def send_mail(subject, recipient, template, **context):
    """
    Workaround for https://github.com/mattupstate/flask-security/issues/693
    """

    context.setdefault('security', _security)
    context.update(_security._run_ctx_processor('mail'))

    msg = Message(subject,
                  sender=str(_security.email_sender),
                  recipients=[recipient])

    ctx = ('security/email', template)
    if config_value('EMAIL_PLAINTEXT'):
        msg.body = render_template('%s/%s.txt' % ctx, **context)
    if config_value('EMAIL_HTML'):
        msg.html = render_template('%s/%s.html' % ctx, **context)

    if _security._send_mail_task:
        _security._send_mail_task(msg)
        return

    mail = security.app.extensions.get('mail')
    mail.send(msg)

def _filter_allowed_scopes(user: User, scopes: List[str]) -> List[str]:
    allowed_scopes: Set[str] = {scope for role in user.roles for scope in role.allowed_scopes}
    return [scope for scope in scopes if scope in allowed_scopes]