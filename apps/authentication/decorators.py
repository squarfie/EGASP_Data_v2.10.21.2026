from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def is_admin_user(user):
    return (
        user.is_authenticated
        and user.is_active
        and (user.is_superuser or user.is_staff)
    )


def admin_required(view_func):
    @login_required(login_url="/login/")
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not is_admin_user(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped_view
