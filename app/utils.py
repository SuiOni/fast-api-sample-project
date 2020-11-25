# import code for encoding urls and generating md5 hashes
import urllib
import hashlib

from app.core.config import settings


def gen_gravatar(email="someone@somewhere.com", size=40):
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(
        email.lower().encode('utf-8')).hexdigest() + "?"
    gravatar_url += urllib.parse.urlencode({'d': settings.GRAVATAR_DEFAULT_URL,
                                            's': str(size)})
    return gravatar_url
