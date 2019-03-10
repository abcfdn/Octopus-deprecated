import requests

def get_content(url, allow_redirects=True):
    r = requests.get(url, allow_redirects=allow_redirects)
    return r.content

def get_content_type(url, allow_redirects=True):
    h = requests.head(url, allow_redirects=True)
    return h.headers.get('content-type')

def get_content_length(url, allow_redirects=True):
    h = requests.head(url, allow_redirects=True)
    return h.headers.get('content-length')
