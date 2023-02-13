from uuid import uuid4
from random import randint

def slugify_url_post() :
    url = str(uuid4())[:23]
    return url

def make_slug_url_comment() :
    slug = randint(1000_000_000_000,9000_000_000_000)
    return slug