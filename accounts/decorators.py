from django.http import JsonResponse
from functools import wraps

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                # For API endpoints, return JSON response
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'success': False,
                        'message': 'Authentication required.'
                    }, status=401)
                # For regular views, render error page
                from django.shortcuts import render
                return render(request, 'error/403.html', status=403)

            # Allow superuser always
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Allow only allowed roles
            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If none match, deny access
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'success': False,
                    'message': 'You do not have permission to access this resource.'
                }, status=403)
            from django.shortcuts import render
            return render(request, 'error/403.html', status=403)
        return _wrapped_view
    return decorator
