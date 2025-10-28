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
                # Check if this is an API request (AJAX, JSON expected, or API path)
                is_api_request = (
                    request.path.startswith('/api/') or
                    request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or
                    'application/json' in request.META.get('HTTP_ACCEPT', '') or
                    request.content_type == 'application/json'
                )

                if is_api_request:
                    return JsonResponse({
                        'success': False,
                        'message': 'Authentication required.'
                    }, status=401)
                # For regular views, redirect to login
                from django.shortcuts import redirect
                return redirect('login')

            # Allow superuser always
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Allow only allowed roles
            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If none match, deny access
            is_api_request = (
                request.path.startswith('/api/') or
                request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or
                'application/json' in request.META.get('HTTP_ACCEPT', '') or
                request.content_type == 'application/json'
            )

            if is_api_request:
                return JsonResponse({
                    'success': False,
                    'message': 'You do not have permission to access this resource.'
                }, status=403)
            from django.shortcuts import render
            return render(request, 'error/403.html', status=403)
        return _wrapped_view
    return decorator

def verified_applications_only(view_func):
    """
    Decorator to ensure only verified applications are returned for certain roles.
    Applies to views that return application querysets.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Call the original view function
        response = view_func(request, *args, **kwargs)

        # If the response is not a JsonResponse or doesn't have applications data, return as-is
        if not hasattr(response, 'content'):
            return response

        try:
            import json
            data = json.loads(response.content)

            if 'applications' in data and isinstance(data['applications'], list):
                user_role = request.user.role

                # Filter applications based on verification status for specific roles
                if user_role in ['dsw', 'exam_controller']:
                    # Only show verified applications for DSW and exam controller
                    filtered_applications = [
                        app for app in data['applications']
                        if app.get('verified', False)
                    ]
                    data['applications'] = filtered_applications
                    return JsonResponse(data)

        except (json.JSONDecodeError, AttributeError):
            # If we can't parse the response, return it unchanged
            pass

        return response
    return _wrapped_view
