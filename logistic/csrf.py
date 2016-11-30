import re
class IgnoreCrsfMiddleware(object):
    def process_request(self, request, **karg):
        URL_LIST = [r'^/a/b/$', r'^/c/d/$',r'[a-zA-z]+://[^\s]*']
        if re.match(u, request.path):
            request.csrf_processing_done = True
            return None
