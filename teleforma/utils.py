import mimetypes
import hashlib
from django.conf import settings

def guess_mimetypes(url):
    url = url.split("?")[0]
    return mimetypes.guess_type(url)[0]

def generate_hash(mid):
    """
    Generate a hash for messages
    """
    mid = "%x" % mid
    msg = '%s-%s' % (settings.SECRET_KEY, mid)
    md5 = hashlib.md5(msg.encode('utf8')).hexdigest()
    return '%s%s' % (mid, md5[:4])
