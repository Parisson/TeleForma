import urllib.parse as urlparse
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect

from .models.crfpa import Student


def user_passes_test(login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            restricted = False
            if user.is_authenticated:
                try:
                    student = user.student.get()
                except Student.DoesNotExist:
                    student = None
                if student:
                    restricted = student.restricted
                if not restricted:
                    return view_func(request, *args, **kwargs)

            if restricted:
                return redirect('teleforma-unauthorized')

            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                           settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def access_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# def access_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
#     """
#     Decorator for views that checks that the user is logged in, redirecting
#     to the log-in page if necessary.
#     """
#     def can_access(user):
#         student = user.student.get()
#         if student:
#             return user.is_authenticated() and not student.restricted
#         return user.is_authenticated()


#     student = user.student.get()
#     if student:
#         if student.restricted:
#             redirect('user-restricted')

#     path = request.build_absolute_uri()
#     # If the login url is the same scheme and net location then just
#     # use the path as the "next" url.
#     login_scheme, login_netloc = urlparse.urlparse(login_url or
#                                                 settings.LOGIN_URL)[:2]
#     current_scheme, current_netloc = urlparse.urlparse(path)[:2]
#     if ((not login_scheme or login_scheme == current_scheme) and
#         (not login_netloc or login_netloc == current_netloc)):
#         path = request.get_full_path()
#     from django.contrib.auth.views import redirect_to_login
#     return redirect_to_login(path, None, redirect_field_name)

#     actual_decorator = user_passes_test(
#         lambda u: can_access(u),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator
