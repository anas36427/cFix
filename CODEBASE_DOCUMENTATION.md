
### Code Execution Flow
The cFix Django application can be started through different entry points depending on the environment:

#### 1. Development Server (manage.py)
**Primary development entry point:**
```bash
python manage.py runserver
```
- **File**: `cFix/manage.py`
- **Purpose**: Starts Django's built-in development server
- **Default URL**: `http://127.0.0.1:8000/`
- **Usage**: For local development and testing

**What happens when you run this:**
1. Django loads settings from `cFix/settings.py`
2. Initializes all INSTALLED_APPS (accounts, seeFix, theme, etc.)
3. Sets up URL routing from `cFix/urls.py`
4. Starts the WSGI application via `cFix/wsgi.py`
5. Serves static files and handles requests

#### 2. Production Server (Gunicorn)
**Production deployment entry point:**
```bash
gunicorn cFix.wsgi
```
- **File**: `cFix/cFix/wsgi.py`
- **Purpose**: Production WSGI server for hosting platforms like Render/Heroku
- **Configuration**: Defined in `Procfile` as `web: gunicorn cFix.wsgi`
- **Usage**: For production deployment

**WSGI Application Flow:**
- `cFix/wsgi.py` creates the WSGI application object
- Gunicorn loads this WSGI app
- All HTTP requests are processed through this entry point

#### 3. ASGI Server (Optional)
**Asynchronous server entry point:**
- **File**: `cFix/cFix/asgi.py`
- **Purpose**: For asynchronous web servers (Daphne, Uvicorn)
- **Usage**: If the application needs async features

### Request Processing Flow
When a user visits the website:

1. **Web Server** (Gunicorn/Development server) receives the HTTP request
2. **WSGI Application** (`wsgi.py`) processes the request
3. **Django URL Router** (`urls.py`) matches the URL to a view
4. **View Function** (in `accounts/views.py` or `cFix/views.py`) processes the request
5. **Template Rendering** (if applicable) uses templates from `templates/`
6. **Database Queries** (if needed) use models from `accounts/models.py`
7. **Response** is sent back through the WSGI pipeline

## Code Execution Process

### Role-Based Code Execution
The application triggers different code paths based on user roles and actions. Here's how the code execution flows for different scenarios:

#### 1. User Authentication Flow
**When a user logs in (`/accounts/login/`):**

```python
# Triggered code in accounts/views.py
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Role-based redirection logic
            if user.role == 'student':
                return redirect('student_dashboard')  # -> student_dashboard view
            elif user.role == 'staff':
                return redirect('staff_dashboard')    # -> staff_dashboard view
            # ... other roles
```

**Backend authentication (`accounts/backends.py`):**
```python
class CollegeIdBackend:
    def authenticate(self, request, college_id=None, password=None):
        # Custom authentication using college_id instead of username
        # Triggers: CustomUser.objects.get(college_id=college_id)
```

#### 2. Student Dashboard Access (`/accounts/dashboard/student/`)
**Triggered Code:**
- **Decorator Check**: `@role_required(['student'])` in `accounts/decorators.py`
- **View Function**: `student_dashboard()` in `accounts/views.py`
- **Template**: `templates/dashboard/student.html`
- **Context Data**: Recent unread notifications from `user.notifications.filter(is_read=False)`

#### 3. Complaint Submission (AJAX POST to `/accounts/complaints/submit/`)
**Triggered Code Sequence:**
1. **URL Routing**: `accounts/urls.py` → `submit_complaint` view
2. **Decorator**: `@role_required(['student'])` + `@csrf_exempt` + `@require_POST`
3. **View Logic** (`accounts/views.py`):
   ```python
   def submit_complaint(request):
       data = json.loads(request.body)
       form = ComplaintForm(data)
       if form.is_valid():
           complaint = form.save(commit=False)
           complaint.student = request.user  # Triggers database save
           complaint.save()
           return JsonResponse({'success': True})
   ```
4. **Model Save**: `Complaint` model triggers database insertion
5. **Response**: JSON response sent back to frontend JavaScript

#### 4. Staff Complaint Management (`/accounts/complaints/all/`)
**Triggered Code:**
- **Role Check**: `@role_required(['staff', 'provost', 'dsw', 'exam_controller'])`
- **View Function**: `all_complaints()` filters by user role:
  ```python
  if user_role == 'staff':
      complaints = Complaint.objects.filter(department='staff')
  elif user_role == 'provost':
      complaints = Complaint.objects.all()  # All complaints
  ```
- **Database Query**: Triggers MongoDB query via Djongo
- **JSON Response**: Formatted complaint data for frontend tables

#### 5. Status Update Actions (AJAX POST)
**Example: Update Complaint Status (`/accounts/complaints/update-status/`):**
```python
def update_complaint_status(request):
    data = json.loads(request.body)
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.status = new_status
    complaint.save()  # Triggers database update
    # Notification creation logic triggered here
```

#### 6. API Endpoints (`/api/` routes)
**Triggered for REST API calls:**
- **Registration**: `seeFix/views.py:RegisterView.post()`
  - Uses MongoEngine `User` model (different from Django CustomUser)
  - Triggers: `User(**data).save()` to MongoDB collection
- **Login**: `seeFix/views.py:LoginView.post()`
  - Triggers: `User.objects(email=data['email']).first()`

#### 7. Database Triggers
**Automatic Code Execution:**
- **Model Save Signals**: Django signals trigger on model save/delete
- **Migration Execution**: `manage.py migrate` triggers schema changes
- **Query Execution**: ORM queries trigger database operations

#### 8. Frontend JavaScript Triggers
**AJAX Calls from `static/script.js`:**
```javascript
// Triggers backend view when form submitted
fetch('/accounts/complaints/submit/', {
    method: 'POST',
    body: JSON.stringify(formData)
}).then(response => {
    // Triggers UI updates based on JSON response
});
```

#### 9. Template Rendering Triggers
**When Templates Load:**
- **Context Processors**: Automatically add user data to all templates
- **Template Tags**: Custom tags in templates trigger Python functions
- **Static File Loading**: Triggers WhiteNoise or Django static file serving

#### 10. Background Tasks (Future Implementation)
**Automatic Deletion (from TODO.md):**
- Would trigger periodic tasks to delete old resolved/rejected items
- Code would run via Django management commands or cron jobs

### Conditional Code Execution Examples

#### Based on User Role:
```python
# In views.py
if request.user.role == 'student':
    # Student-specific code triggered
    notifications = request.user.notifications.filter(is_read=False)
elif request.user.role == 'provost':
    # Provost-specific code triggered
    applications = Application.objects.filter(verified=False)
```

#### Based on Request Type:
```python
# AJAX vs Regular requests
is_api_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
if is_api_request:
    # JSON response code triggered
    return JsonResponse(data)
else:
    # Template rendering code triggered
    return render(request, 'template.html', context)
```

#### Based on HTTP Method:
```python
if request.method == 'GET':
    # Data retrieval code triggered
    return render(request, 'form.html')
elif request.method == 'POST':
    # Data processing code triggered
    form = Form(request.POST)
    if form.is_valid():
        form.save()  # Database save triggered
```

This role-based and action-based code execution ensures that only relevant code runs for each user type and scenario, maintaining security and performance.

### Key Starting Files
- **`manage.py`**: Development command runner
- **`cFix/wsgi.py`**: Production WSGI entry point
- **`cFix/asgi.py`**: Asynchronous server entry point
- **`cFix/settings.py`**: Configuration loaded at startup
- **`cFix/urls.py`**: URL routing loaded at startup

## Django Management Commands

### manage.py Usage
`manage.py` is Django's command-line utility that provides various administrative commands for the project. Located in the root directory, it should be executed from the project root.

### Common Commands

#### Development Server
```bash
python manage.py runserver
```
Starts the development server on `http://127.0.0.1:8000/` (default). Use `python manage.py runserver 8080` to specify a port.

#### Database Operations
```bash
python manage.py makemigrations
```
Creates new migration files based on model changes.

```bash
python manage.py migrate
```
Applies pending migrations to the database.

```bash
python manage.py showmigrations
```
Displays the status of all migrations.

#### Data Management
```bash
python manage.py createsuperuser
```
Creates a superuser account for admin access.

```bash
python manage.py shell
```
Opens an interactive Python shell with Django context.

```bash
python manage.py dbshell
```
Opens the database shell for direct database queries.

#### Static Files
```bash
python manage.py collectstatic
```
Collects all static files into the `STATIC_ROOT` directory for production.

#### Testing
```bash
python manage.py test
```
Runs all tests in the project.

```bash
python manage.py test accounts
```
Runs tests for the accounts app only.

#### Production Checks
```bash
python manage.py check --deploy
```
Performs production readiness checks.

#### Custom Commands
The project supports custom management commands (located in `accounts/management/commands/`):
- Currently no custom commands are implemented
- To create a custom command: `python manage.py startapp management/commands/your_command.py`

### Command Execution Context
All commands should be run from the project root directory (`cFix/`) with the virtual environment activated. The commands automatically use the settings defined in `cFix/settings.py`.

## Deployment Issues & Troubleshooting

### Render Deployment Errors & Fixes

#### 1. **Environment Variables Missing**
**Error:** Application crashes on startup due to missing `SECRET_KEY` or `MONGO_URI`

**Symptoms:**
- Build succeeds but runtime fails
- Logs show: "SECRET_KEY not found" or "MONGO_URI not found"

**Fix:**
- Ensure these environment variables are set in Render dashboard:
  - `SECRET_KEY`: A long random string (generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
  - `MONGO_URI`: Full MongoDB Atlas connection string
  - `MONGO_DB_NAME`: Database name (e.g., "cfix_db")
  - `DEBUG`: Set to "False" for production

#### 2. **MongoDB Connection Issues**
**Error:** "Connection refused" or "Authentication failed" to MongoDB

**Common Causes:**
- Incorrect MongoDB Atlas connection string
- IP whitelist not configured in MongoDB Atlas
- Database user credentials incorrect
- Network restrictions

**Fix:**
- Verify MongoDB Atlas connection string format:
  ```
  mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
  ```
- Add `0.0.0.0/0` to IP whitelist in MongoDB Atlas (temporary for testing)
- Ensure database user has read/write permissions

#### 3. **Static Files Not Loading**
**Error:** CSS/JS files return 404 in production

**Symptoms:**
- Site loads but styling is broken
- Console shows 404 errors for static files

**Fix:**
- Ensure `python manage.py collectstatic` runs during build
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise middleware is properly configured
- Confirm static files are in `static/` directory

#### 4. **Django Migrations Pending**
**Error:** "You have unapplied migrations" on startup

**Symptoms:**
- Application starts but database schema is outdated
- Features may not work correctly

**Fix:**
- Add migration command to build process:
  ```bash
  python manage.py migrate
  ```
- Or ensure migrations are committed and up-to-date

#### 5. **Python Version Mismatch**
**Error:** "Python version not supported" or import errors

**Symptoms:**
- Build fails with Python compatibility issues
- Dependencies fail to install

**Fix:**
- `runtime.txt` specifies Python 3.12.7
- Ensure all dependencies in `requirements.txt` are compatible with Python 3.12
- Check for deprecated packages (Django 3.2.25 is used for Djongo compatibility)

#### 6. **WSGI Application Errors**
**Error:** Gunicorn fails to start or "application not found"

**Symptoms:**
- "Failed to find application" in logs
- WSGI import errors

**Fix:**
- Verify `Procfile` content: `web: gunicorn cFix.wsgi`
- Check `cFix/wsgi.py` has correct `DJANGO_SETTINGS_MODULE`
- Ensure `cFix/wsgi.py` is in the correct location

#### 7. **ALLOWED_HOSTS Configuration**
**Error:** "DisallowedHost" exception

**Symptoms:**
- 400 Bad Request errors
- Site inaccessible

**Fix:**
- Update `ALLOWED_HOSTS` in `settings.py` with your Render domain:
  ```python
  ALLOWED_HOSTS = [
      'your-app-name.onrender.com',
      'localhost',
      '127.0.0.1',
  ]
  ```

#### 8. **CSRF Trusted Origins**
**Error:** CSRF verification failed

**Symptoms:**
- POST requests fail with CSRF errors
- Forms don't submit

**Fix:**
- Add your Render domain to `CSRF_TRUSTED_ORIGINS`:
  ```python
  CSRF_TRUSTED_ORIGINS = [
      'https://your-app-name.onrender.com',
  ]
  ```

#### 9. **Database Schema Issues**
**Error:** Model fields don't match database or migration conflicts

**Symptoms:**
- FieldDoesNotExist errors
- Inconsistent data

**Fix:**
- Ensure all migrations are applied: `python manage.py migrate`
- Check model definitions match database schema
- Reset database if schema is corrupted (last resort)

#### 10. **Memory/Timeout Issues**
**Error:** Application times out or runs out of memory

**Symptoms:**
- 504 Gateway Timeout
- Build fails with memory errors

**Fix:**
- Optimize database queries (use select_related, pagination)
- Reduce static file size
- Check for memory leaks in code
- Consider upgrading Render plan for more resources

### Pre-Deployment Checklist

#### Environment Setup
- [ ] `SECRET_KEY` environment variable set
- [ ] `MONGO_URI` environment variable set
- [ ] `MONGO_DB_NAME` environment variable set
- [ ] `DEBUG=False` for production

#### Database Configuration
- [ ] MongoDB Atlas cluster created
- [ ] Database user with read/write permissions
- [ ] IP whitelist configured (or 0.0.0.0/0 for testing)
- [ ] Connection string tested locally

#### Code Preparation
- [ ] All migrations committed
- [ ] `requirements.txt` updated with correct versions
- [ ] `ALLOWED_HOSTS` includes Render domain
- [ ] `CSRF_TRUSTED_ORIGINS` includes Render domain
- [ ] Static files committed (or collected during build)

#### Build Configuration
- [ ] `Procfile` contains: `web: gunicorn cFix.wsgi`
- [ ] `runtime.txt` specifies: `python-3.12.7`
- [ ] Build command includes: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`

### Common Render-Specific Issues

#### Build Failures
- **Large repository:** Remove unnecessary files (.git, node_modules, etc.)
- **Dependency conflicts:** Use compatible package versions
- **Disk space:** Clean up build artifacts

#### Runtime Issues
- **Cold starts:** Expected on free tier, may take 30+ seconds
- **File system:** Read-only except `/tmp`, don't write files
- **Environment variables:** Case-sensitive, check spelling

#### Monitoring & Debugging

##### **Accessing Render Logs**
- **Real-time Logs:** In Render dashboard, go to your service → "Logs" tab to view live application logs
- **Build Logs:** Check build process logs for dependency installation and migration errors
- **Runtime Logs:** Monitor application startup, database connections, and runtime errors
- **Filter Logs:** Use search functionality to filter by keywords like "ERROR", "WARNING", "MongoDB"

##### **Local Testing with Production Settings**
Before deploying, test locally with production-like settings:

```bash
# Create a .env.production file with production values
cp .env.example .env.production

# Run with production settings
DEBUG=False python manage.py runserver

# Test database connection
python manage.py dbshell  # For MongoDB, this may not work with Djongo

# Test static file collection
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
```

##### **Database Connection Testing**
```python
# Add this to a Django shell to test MongoDB connection
python manage.py shell
>>> from django.db import connection
>>> connection.cursor()  # Should not raise errors
>>> from accounts.models import CustomUser
>>> CustomUser.objects.all()[:1]  # Test a simple query
```

##### **Static Files Debugging**
- Check if `STATIC_ROOT` directory exists and contains files after `collectstatic`
- Verify `STATIC_URL` is correctly set
- Test static file serving: Visit `https://your-app.onrender.com/static/style.css`
- Ensure WhiteNoise is properly configured in middleware

##### **Performance Monitoring**
- **Response Times:** Use browser dev tools to check page load times
- **Database Queries:** Enable Django debug toolbar locally (not in production)
- **Memory Usage:** Monitor Render metrics for memory consumption
- **Cold Starts:** Free tier has cold starts; expect 10-30 second delays

##### **Error Tracking & Alerting**
- **Django Error Pages:** Temporarily set `DEBUG=True` to see detailed error pages
- **Custom Error Logging:** Add logging to critical functions:
  ```python
  import logging
  logger = logging.getLogger(__name__)

  def my_view(request):
      try:
          # your code
          pass
      except Exception as e:
          logger.error(f"Error in my_view: {e}")
          raise
  ```
- **Sentry Integration:** Consider adding Sentry for production error tracking

##### **Health Check Endpoints**
Add a health check view for monitoring:

```python
# In views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Test database connection
        connection.cursor()
        return JsonResponse({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'database': str(e)}, status=500)
```

Add to `urls.py`:
```python
path('health/', views.health_check, name='health_check'),
```

##### **Debugging Checklist**
- [ ] Check Render service status and metrics
- [ ] Review recent deployments and rollback if needed
- [ ] Verify environment variables are set correctly
- [ ] Test database connectivity from Render
- [ ] Check static file accessibility
- [ ] Monitor error logs for patterns
- [ ] Test critical user flows manually
- [ ] Verify third-party services (MongoDB Atlas) are operational

##### **Common Debug Commands**
```bash
# Check Django settings
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES)"

# Test MongoDB connection directly
python -c "import pymongo; client = pymongo.MongoClient('your_mongo_uri'); print(client.list_database_names())"

# Check installed packages
pip list | grep -E "(Django|djongo|mongo)"

# Validate requirements compatibility
pip check
```

##### **Troubleshooting Workflow**
1. **Check Logs First:** Always start with Render logs
2. **Reproduce Locally:** Try to replicate the issue in local development
3. **Isolate Components:** Test database, static files, and views separately
4. **Check Configuration:** Verify all settings match production requirements
5. **Incremental Changes:** Make one change at a time and redeploy
6. **Rollback Plan:** Have a known good deployment to rollback to
7. **External Factors:** Check if issues are due to MongoDB Atlas, network, or Render platform

##### **Advanced Debugging**
- **Remote Debugging:** Use `pdb` or `ipdb` in code (not recommended for production)
- **Database Profiling:** Monitor slow queries with MongoDB profiler
- **Load Testing:** Use tools like Locust to test under load
- **Browser DevTools:** Check network tab for failed requests
- **API Testing:** Use Postman or curl to test endpoints directly

This documentation provides a comprehensive overview of the cFix codebase architecture, functionality, and implementation details for development and maintenance purposes.
