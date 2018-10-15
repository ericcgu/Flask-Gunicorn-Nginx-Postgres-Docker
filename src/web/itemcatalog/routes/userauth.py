from flask import Blueprint, redirect, url_for, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_login import current_user, login_user, logout_user
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from oauthlib.oauth2.rfc6749.errors import InvalidClientIdError
from itemcatalog import app, db, user

userauth = Blueprint('userauth', __name__)

app.secret_key = app.config['GOOGLE_OAUTH_CLIENT_SECRET']

google_blueprint = make_google_blueprint(
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.secret_key,
    scope=app.config['GOOGLE_OAUTH_CLIENT_SCOPE'],
    offline=True
    )

google_blueprint.backend = SQLAlchemyBackend(user.UserAuth, db.session,
                                             user=current_user,
                                             user_required=False)

app.register_blueprint(google_blueprint, url_prefix="/google_login")


@userauth.route("/google_login")
def google_login():
    """redirect to Google to initiate oAuth2.0 dance"""
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return resp.text


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    """
    Receives a signal that Google has authenticated User via
    instance of blueprint and token
        1. Check response from instance of blueprint
        2. Check if user exists from db via email
        3. Create user in db if user does not exist
    """
    from itemcatalog import user
    User = user.User
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if resp.ok:
        account_info_json = resp.json()
        email = account_info_json['email']
        query = User.query.filter_by(email=email)

        try:
            user = query.one()
        except NoResultFound:
            user = User()
            user.name = account_info_json['name']
            user.email = account_info_json['email']
            db.session.add(user)
            db.session.commit()
        login_user(user, remember=True)


@userauth.route('/google_logout')
def google_logout():
    """Revokes token and empties session."""
    if google.authorized:
        try:
            google.get(
                'https://accounts.google.com/o/oauth2/revoke',
                params={
                    'token':
                    google.token['access_token']},
            )
        except InvalidClientIdError:
            """Revokes token and empties session."""
            del google.token
            redirect(url_for('main.index'))
    session.clear()
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.index'))
