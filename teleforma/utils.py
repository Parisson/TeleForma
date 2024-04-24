import mimetypes

def guess_mimetypes(url):
    url = url.split("?")[0]
    return mimetypes.guess_type(url)[0]