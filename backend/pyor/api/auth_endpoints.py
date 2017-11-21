from flask import request, render_template, Blueprint
from flask_login import login_required, current_user

from pyor.api.auth import oauth, _filter_allowed_scopes
from pyor.models import Client

auth_bp = Blueprint('auth', __name__, template_folder="templates")

@auth_bp.route('/oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id: str = kwargs.get('client_id')
        client = Client.objects(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = current_user
        kwargs['scopes'] = _filter_allowed_scopes(current_user, kwargs["scopes"])
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@auth_bp.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None


@auth_bp.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    pass