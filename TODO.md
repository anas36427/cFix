#a TODO: Implement Delete Functionality for Complaints and Applications

## Overview
Implement manual delete views for students to delete their own complaints and applications, but only if status is 'pending', 'resolved', or 'rejected'. Later, add automatic deletion after 10 days.

## Steps
1. [x] Add delete_complaint view in accounts/views.py
   - AJAX POST endpoint
   - Validate ownership and status
   - Delete if allowed
2. [x] Add delete_application view in accounts/views.py
   - Similar to delete_complaint
3. [x] Update accounts/urls.py to include new paths for delete endpoints
4. [x] Fix application submission (remove file input)
5. [x] Add application_details view
6. [x] Add view buttons functionality for complaints and applications
7. [x] Test the delete endpoints (manually or via API calls) - GET endpoints work, POST needs authentication
8. [] (Future) Implement automatic deletion after 10 days for pending, resolved, rejected items
