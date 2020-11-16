# import code for encoding urls and generating md5 hashes
import urllib, hashlib

# Set your variables here
email = "someone@somewhere.com"
default = "https://www.gravatar.com/avatar/00000000000000000000000000000000"
size = 40

# construct the url


def genAvatar(email, size=40):
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(
        email.lower().encode('utf-8')).hexdigest() + "?"
    gravatar_url += urllib.parse.urlencode({'d': default, 's': str(size)})
    return gravatar_url
