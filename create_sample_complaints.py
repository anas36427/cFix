import os
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cFix.settings')
django.setup()

from accounts.models import Complaint, CustomUser

def create_sample_students():
    """Create sample students if they don't exist"""
    students_data = [
        {'email': 'student1@amu.ac.in', 'college_id': 'STU001', 'first_name': 'Ahmed', 'last_name': 'Khan', 'role': 'student'},
        {'email': 'student2@amu.ac.in', 'college_id': 'STU002', 'first_name': 'Fatima', 'last_name': 'Begum', 'role': 'student'},
        {'email': 'student3@amu.ac.in', 'college_id': 'STU003', 'first_name': 'Mohammed', 'last_name': 'Ali', 'role': 'student'},
        {'email': 'student4@amu.ac.in', 'college_id': 'STU004', 'first_name': 'Aisha', 'last_name': 'Siddiqui', 'role': 'student'},
        {'email': 'student5@amu.ac.in', 'college_id': 'STU005', 'first_name': 'Rahul', 'last_name': 'Sharma', 'role': 'student'},
        {'email': 'student6@amu.ac.in', 'college_id': 'STU006', 'first_name': 'Priya', 'last_name': 'Verma', 'role': 'student'},
        {'email': 'student7@amu.ac.in', 'college_id': 'STU007', 'first_name': 'Arjun', 'last_name': 'Patel', 'role': 'student'},
        {'email': 'student8@amu.ac.in', 'college_id': 'STU008', 'first_name': 'Zara', 'last_name': 'Malik', 'role': 'student'},
        {'email': 'student9@amu.ac.in', 'college_id': 'STU009', 'first_name': 'Vikram', 'last_name': 'Singh', 'role': 'student'},
        {'email': 'student10@amu.ac.in', 'college_id': 'STU010', 'first_name': 'Meera', 'last_name': 'Gupta', 'role': 'student'},
    ]

    students = []
    for data in students_data:
        student, created = CustomUser.objects.get_or_create(
            email=data['email'],
            defaults={
                'college_id': data['college_id'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': data['role'],
                'is_active': True,
                'is_verified': True
            }
        )
        if created:
            student.set_password('password123')
            student.save()
        students.append(student)

    return students

def create_sample_complaints():
    """Create 20 diverse sample complaints"""

    # Sample complaint data
    complaint_templates = [
        # Staff/General complaints (5)
        {
            'title': 'WiFi connectivity issues in library',
            'description': 'The WiFi connection in the central library is very slow and keeps disconnecting frequently. This is affecting our study sessions.',
            'category': 'infrastructure',
            'department': 'staff',
            'hall': 'nrsc',
            'priority': 'high'
        },
        {
            'title': 'Broken water cooler in cafeteria',
            'description': 'The water cooler in the main cafeteria has been out of order for the past week. Students are facing difficulty getting drinking water.',
            'category': 'maintenance',
            'department': 'staff',
            'hall': 'nrsc',
            'priority': 'medium'
        },
        {
            'title': 'Parking space shortage',
            'description': 'There is insufficient parking space for students and faculty vehicles during peak hours. This causes traffic congestion.',
            'category': 'infrastructure',
            'department': 'staff',
            'hall': 'nrsc',
            'priority': 'medium'
        },
        {
            'title': 'Lost and found service improvement',
            'description': 'The lost and found service needs better organization and a dedicated space for storing found items.',
            'category': 'other',
            'department': 'staff',
            'hall': 'nrsc',
            'priority': 'low'
        },
        {
            'title': 'Campus security concerns',
            'description': 'Street lights in the parking area are not working properly, creating safety concerns during evening hours.',
            'category': 'security',
            'department': 'staff',
            'hall': 'nrsc',
            'priority': 'high'
        },

        # Provost/Hall Management complaints (5)
        {
            'title': 'Room cleaning schedule irregularity',
            'description': 'The room cleaning service in Aftab Hall is not following the regular schedule. Rooms are not cleaned on time.',
            'category': 'maintenance',
            'department': 'provost',
            'hall': 'aftab',
            'priority': 'medium'
        },
        {
            'title': 'Mess food quality issues',
            'description': 'The food quality in the mess has deteriorated significantly. Meals are often cold and not properly cooked.',
            'category': 'food',
            'department': 'provost',
            'hall': 'ambedkar',
            'priority': 'high'
        },
        {
            'title': 'Laundry service delays',
            'description': 'The laundry service is taking too long to return clothes. Students are facing inconvenience due to this delay.',
            'category': 'other',
            'department': 'provost',
            'hall': 'hadi-hasan',
            'priority': 'medium'
        },
        {
            'title': 'Common room facilities inadequate',
            'description': 'The common room in the hall lacks proper recreational facilities and study spaces for students.',
            'category': 'infrastructure',
            'department': 'provost',
            'hall': 'mohsinul-mulk',
            'priority': 'low'
        },
        {
            'title': 'Hall maintenance urgent repairs',
            'description': 'Several electrical outlets in the rooms are not working. This is creating safety hazards and inconvenience.',
            'category': 'maintenance',
            'department': 'provost',
            'hall': 'mohd-habib',
            'priority': 'urgent'
        },

        # DSW/Student Welfare complaints (5)
        {
            'title': 'Mental health support services',
            'description': 'Students need better access to counseling and mental health support services. Current facilities are inadequate.',
            'category': 'other',
            'department': 'dsw',
            'hall': 'sir-syed-north',
            'priority': 'high'
        },
        {
            'title': 'Financial aid application process',
            'description': 'The process for applying for financial aid and scholarships is too complicated and time-consuming.',
            'category': 'other',
            'department': 'dsw',
            'hall': 'sir-syed-south',
            'priority': 'medium'
        },
        {
            'title': 'Sports facilities improvement',
            'description': 'The sports facilities and equipment need upgrading. Current facilities are not sufficient for all students.',
            'category': 'infrastructure',
            'department': 'dsw',
            'hall': 'viqarul-mulk',
            'priority': 'medium'
        },
        {
            'title': 'Student grievance redressal system',
            'description': 'The current system for addressing student grievances is not effective and needs improvement.',
            'category': 'other',
            'department': 'dsw',
            'hall': 'abdullah',
            'priority': 'high'
        },
        {
            'title': 'Medical facilities accessibility',
            'description': 'The campus medical center has limited hours and insufficient staff to handle student health needs.',
            'category': 'other',
            'department': 'dsw',
            'hall': 'bibi-fatima',
            'priority': 'urgent'
        },

        # Exam Controller complaints (5)
        {
            'title': 'Examination hall seating arrangement',
            'description': 'The seating arrangement in examination halls is not proper, causing confusion and discomfort during exams.',
            'category': 'infrastructure',
            'department': 'exam_controller',
            'hall': 'nrsc',
            'priority': 'high'
        },
        {
            'title': 'Online examination platform issues',
            'description': 'The online examination platform frequently crashes and has technical issues during important exams.',
            'category': 'infrastructure',
            'department': 'exam_controller',
            'hall': 'nrsc',
            'priority': 'urgent'
        },
        {
            'title': 'Question paper distribution delays',
            'description': 'Question papers are not distributed on time in some examination halls, causing unnecessary stress.',
            'category': 'other',
            'department': 'exam_controller',
            'hall': 'nrsc',
            'priority': 'high'
        },
        {
            'title': 'Examination invigilation problems',
            'description': 'There are not enough invigilators in large examination halls, leading to supervision issues.',
            'category': 'other',
            'department': 'exam_controller',
            'hall': 'nrsc',
            'priority': 'medium'
        },
        {
            'title': 'Result declaration delays',
            'description': 'Examination results are declared very late, affecting students\' academic planning and career decisions.',
            'category': 'other',
            'department': 'exam_controller',
            'hall': 'nrsc',
            'priority': 'medium'
        }
    ]

    # Create students first
    students = create_sample_students()

    # Create complaints
    created_complaints = []
    for i, template in enumerate(complaint_templates):
        # Randomly select a student
        student = random.choice(students)

        # Random status with weighted distribution
        status_weights = [('pending', 40), ('in-progress', 30), ('resolved', 25), ('rejected', 5)]
        status = random.choices([s[0] for s in status_weights], weights=[s[1] for s in status_weights])[0]

        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        created_date = datetime.now() - timedelta(days=days_ago)

        complaint = Complaint.objects.create(
            title=template['title'],
            description=template['description'],
            category=template['category'],
            department=template['department'],
            hall=template['hall'],
            priority=template['priority'],
            status=status,
            student=student,
            created_at=created_date,
            updated_at=created_date + timedelta(hours=random.randint(1, 24))
        )

        created_complaints.append(complaint)
        print(f"Created complaint {i+1}: {complaint.title} (Department: {complaint.department}, Status: {complaint.status})")

    return created_complaints

if __name__ == '__main__':
    print("Creating sample complaints...")
    complaints = create_sample_complaints()
    print(f"\nSuccessfully created {len(complaints)} sample complaints!")

    # Print summary by department
    departments = ['staff', 'provost', 'dsw', 'exam_controller']
    for dept in departments:
        count = Complaint.objects.filter(department=dept).count()
        print(f"{dept.title()}: {count} complaints")
