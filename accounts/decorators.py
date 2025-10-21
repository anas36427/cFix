from django.shortcuts import render
from functools import wraps

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                # Redirect or deny if not logged in
                return render(request, 'errors/403.html', status=403)

            # Allow superuser always
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Allow only allowed roles
            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If none match, deny access
            return render(request, 'errors/403.html', status=403)
        return _wrapped_view
    return decorator
