import oauth2
from urllib.parse import parse_qsl

import constants


# Create a consumer to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

class TwitterUtils:
    global consumer

    @classmethod
    def get_request_token(cls):
        client = oauth2.Client(consumer)

        # Use the client token parsing the query string returned
        response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
        if response.status == 200:
            return dict(parse_qsl(content.decode('utf-8')))

        print('An error has occurred getting the request token from twitter.')

    @classmethod
    def get_oauth_verifier(cls, request_token):
        # Ask the user to authorize our app and give us the pin code
        print('Go to the following site in your browser:')
        print(cls.get_oauth_verifier_url(request_token))

        return input('What is the PIN?:  ')

    @classmethod
    def get_oauth_verifier_url(cls, request_token):
        return f"{constants.AUTHORIZATION_URL}?oauth_token={request_token['oauth_token']}"
        
    @classmethod
    def get_access_token(cls, request_token, oauth_verifier):
        # Create a Token  object which contains the request token, and the verifier
        token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)

        # Create a client with our consumer (our app) and the newly created (and verified) token
        client = oauth2.Client(consumer, token)

        # Ask Twitter for an access token, and Twitter knows that it should give it because we've verified the request token
        response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
        return dict(parse_qsl(content.decode('utf-8')))