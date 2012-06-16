from flask import Flask, redirect, url_for, session, request, Response
from flaskext.oauth import OAuth
import json


SECRET_KEY = 'development key'
DEBUG = True
GITHUB_APP_ID = '60c67e0022bdd775523e'
GITHUB_APP_SECRET = '88a87232c104539d4a1c54f3a7359040483195c3'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

github = oauth.remote_app('github',
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    consumer_key=GITHUB_APP_ID,
    consumer_secret=GITHUB_APP_SECRET,
    request_token_params={'scope': 'user'}
)


@app.route('/')
def index():
    print session
    if 'oauth_token' not in session:
        return redirect(url_for('login'))
    else:
        return Response(
            json.dumps(session['user'], ensure_ascii=False, indent = True),
            mimetype='application/json'
        )


@app.route('/login')
def login():
    return github.authorize(callback=url_for('github_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@github.authorized_handler
def github_authorized(resp):
    if resp is None:
        return 'Access denied: error=%s' % (
            request.args['error'],
        )
    session['oauth_token'] = (resp['access_token'], '')
    user = github.get('user')
    session['user'] = dict(user.data)
    return redirect('/')


@github.tokengetter
def get_github_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
