import requests
from flask import Flask, render_template, session, redirect, request, url_for, g

from twitter_utils import TwitterUtils
from user import User
from database import Database

app = Flask(__name__)
app.secret_key = 'e2vyU5qbyUaDknVG'

Database.initialize(user='postgres', password='alphacharlie73', host='192.168.100.172', database='learning')

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))

    request_token = TwitterUtils.get_request_token()
    session['request_token'] = request_token

    return redirect(TwitterUtils.get_oauth_verifier_url(request_token))

@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = TwitterUtils.get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if user is None:
        user = User(
            access_token['screen_name'],
            access_token['oauth_token'],
            access_token['oauth_token_secret']
        )
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)

@app.route('/logout')
def logout():
    session.clear()

    return url_for('home')

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request(f'https://api.twitter.com/1.1/search/tweets.json?q={query}')

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_texts:
        sentament_info = requests.post('http://text-processing.com/api/sentiment/', data={'text':tweet['tweet']})
        json_response = sentament_info.json()
        label = json_response['label']
        tweet['label'] = label

    return render_template('search.html', content=tweet_texts)

app.run(port=4995, debug=True)