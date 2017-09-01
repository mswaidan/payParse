from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException


FACEBOOK_APP_ID = 'x862s0kv8fbmgg5fnrbqmnas'
FACEBOOK_APP_SECRET = 'e9a9gmw2n6'


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'listings_r'},
    base_url='https://openapi.etsy.com/v2',
    request_token_url='/oauth/request_token',
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://etsy.com/oauth/signin'
)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)


@app.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()

