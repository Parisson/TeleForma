import mimetypes

def guess_mimetypes(path):
    try:
        path = path.decode()
    except (UnicodeDecodeError, AttributeError):
        pass
    return mimetypes.guess_type(path)[0]