

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.urls import path
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static


def error_content(status: int):
    if status == 403:
        text = ' Permission Denied'
    elif status == 404:
        text = ' Not Found'
    else:
        text = ''
    html = f'<html>\
            <body>\
                <div style="text-align:center">\
                <b style="font-size:30px">\
                    ({status}){text}\
                </b>\
                </div>\
            </body>\
            </html>'
    return html


def permission_denied_view(request):
    raise PermissionDenied()

def not_found_view(request):
    raise Http404()

def permission_denied_error_handler(request, exception=None):
    return HttpResponse(error_content(status=403), status=403)

def not_found_error_handler(request, exception=None):
    return HttpResponse(error_content(status=404), status=404)

def _static_butler(request, path, **kwargs):
    """
    Serve static files using the django static files configuration
    WITHOUT collectstatic. This is slower, but very useful for API 
    only servers where the static files are really just for /admin

    Passing insecure=True allows serve_static to process, and ignores
    the DEBUG=False setting
    """
    return serve_static(request, path, insecure=True, **kwargs)


urlpatterns = [
    path('403/', permission_denied_view),
    path('404/', not_found_view),
    path('admin/', admin.site.urls),
    path('api/authtoken/', include('authtoken.api.urls')),
    path('api/cbers-cc-plugin/', include('cbers_cc_plugin.api.urls')),
]

if not settings.DEBUG:
    urlpatterns.append(re_path(r'static/(.+)', _static_butler))

handler403 = permission_denied_error_handler
handler404 = not_found_error_handler
