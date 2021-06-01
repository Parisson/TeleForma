# postman should use dj_pagination when installed but that's not the case here.
# Instead it uses its dj_pagination mock functions.
# So here we replace the pagination_tags templatetags of postman by those of dj_pagination.
import sys
sys.modules['postman.templatetags.pagination_tags'] = __import__('dj_pagination.templatetags.pagination_tags')
