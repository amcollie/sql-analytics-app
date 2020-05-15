from user import User
from database import Database
from twitter_utils import TwitterUtils


Database.initialize(user='postgres', password='alphacharlie73', host='192.168.100.172', database='learning')
email = input('Please enter your email: ')
user = User.load_from_db_by_email(email)



if user is None:
    request_token = TwitterUtils.get_request_token()

    oauth_verifier = TwitterUtils.get_oauth_verifier(request_token)

    access_token = TwitterUtils.get_access_token(request_token, oauth_verifier)

    first_name = input('Please enter your first name: ')
    last_name = input('Please enter your last name: ')


    user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'])
    user.save_to_db()


tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

if tweets:
    for tweet in tweets['status']:
        print(tweet['text'])

