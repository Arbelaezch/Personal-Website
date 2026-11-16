from django.conf import settings

# One policy for the public pages: everything comes from this site. Inline style attributes are
# allowed because the rich-text editor writes them (text alignment, image width); inline scripts
# and inline <style> blocks are not, and the templates have none.
CONTENT_SECURITY_POLICY = '; '.join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self'",
    "style-src-attr 'unsafe-inline'",
    "img-src 'self' data:",
    "font-src 'self'",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
])

# The admin, the editor and the browsable API bring their own inline scripts and styles.
EXEMPT_PREFIXES = ('/admin/', '/ckeditor5/', '/api/', '/api-auth/')


class ContentSecurityPolicyMiddleware:
    """Adds the Content-Security-Policy header to public pages.

    settings.CSP_MODE: "report-only" (browsers log violations, block nothing), "enforce" or "off".
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        mode = settings.CSP_MODE
        if mode == 'off' or request.path.startswith(EXEMPT_PREFIXES):
            return response
        header = 'Content-Security-Policy' if mode == 'enforce' else 'Content-Security-Policy-Report-Only'
        response.setdefault(header, CONTENT_SECURITY_POLICY)
        return response
