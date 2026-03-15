Django Accounts and Reports Management System

Welcome to the Django Accounts and Reports Management System, a comprehensive web application developed during a one-month internship at APDCL Bijulee Bhawan. This project showcases the practical implementation of Django framework concepts, demonstrating secure user management, OTP verification, and administrative workflows.

Internship Project Details:
- Developed under the guidance of Mr. Anshuman Rajkonwar at APDCL Bijulee Bhawan
- Intern: Ronit Chakraborty from Assam Kaziranga University, Department of Computer Science Engineering
- Duration: One month
- Team Member: Rittik Das

Project Overview:
This Django-based application provides a complete solution for user registration, verification, and financial report submission with robust admin approval mechanisms. Built with modern web development practices, it features a custom user model, secure authentication, and an intuitive admin interface.

Key Features:
• Secure user registration with OTP verification for both email and phone
• Custom user model with unique registration numbers, address management, and verification statuses
• Financial report submission system with comprehensive bank details and approval workflow
• Dedicated admin dashboard for managing user registrations and report approvals
• Personal user dashboard for profile management and report tracking
• Responsive design with clean HTML/CSS templates
• Comprehensive status management for users and reports

Technology Stack:
• Backend: Django 4.x framework
• Database: SQLite (default), configurable for PostgreSQL/MySQL
• Frontend: HTML5, CSS3 with Django Templates
• Authentication: Django's built-in auth system with custom user model
• Email: Console backend for development, SMTP configurable for production
• Python Version: 3.8+

Installation Guide:

Prerequisites:
- Python 3.8 or higher
- pip package installer
- Virtual environment (recommended)

Setup Steps:

1. Clone the repository to your local machine
2. Create and activate a virtual environment
3. Install Django and required dependencies
4. Apply database migrations
5. Create a superuser account for admin access
6. Launch the development server
7. Access the application at http://127.0.0.1:8000/

How It Works:

User Registration Process:
Users begin by completing a registration form with their personal details. The system then sends OTP codes to both their email and phone for verification. Once verified, accounts enter a pending status until administrative approval, ensuring a secure and controlled registration workflow.

Report Submission System:
Authenticated users can submit detailed financial reports including transaction dates, amounts, bank information, and descriptions. All reports start in a pending state, requiring admin review and approval before final processing.

Administrative Capabilities:
Administrators have full control over the system, with the ability to approve or reject user registrations, manage report submissions, and block or unblock user accounts as needed. The Django admin interface provides comprehensive management tools.

Project Architecture:

The application follows Django's MTV (Model-Template-View) architecture with a clean, modular structure:

- accounts/ - Core application handling user management and reports
- apple/ - Project configuration and settings
- templates/ - HTML templates for the user interface
- static/ - CSS, JavaScript, and media files
- Database migrations and management scripts

Configuration Options:

For production deployment, the application supports various configuration options including SMTP email settings, database connections (PostgreSQL/MySQL), and security settings. The settings.py file provides clear documentation for all configuration parameters.

Learning Experience:

This internship project provided valuable hands-on experience in:
- Django framework architecture and best practices
- Custom user authentication and authorization
- Database modeling and migrations
- Web interface development with responsive design
- Project management and version control
- Team collaboration and code development workflows

Contributing:
We welcome contributions to improve the project. Please follow standard Git workflow practices, create feature branches, and submit pull requests for review.

Testing:
Run the test suite using Django's built-in testing framework to ensure code quality and functionality.

Deployment:
For production environments, configure proper security settings, database connections, and static file serving. The application is ready for deployment on various hosting platforms.

License:
This project is released under the MIT License, allowing for free use and modification.

Acknowledgments:
Special thanks to Mr. Anshuman Rajkonwar for his guidance and mentorship during the internship at APDCL Bijulee Bhawan. Gratitude to Assam Kaziranga University for the educational foundation, and to team member Rittik Das for the collaborative development experience. This project stands as a testament to the power of practical learning in computer science education.

Contact Information:
For questions or feedback about this internship project, please reach out through appropriate channels.

This project represents the culmination of a one-month internship experience, bridging academic knowledge with real-world application development at APDCL Bijulee Bhawan.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Endpoints

- `/` - Home/Register page
- `/login/` - User login
- `/dashboard/` - User dashboard
- `/submit-report/` - Report submission form
- `/my-reports/` - User's reports
- `/admin/` - Django admin interface

## Learning Outcomes

This internship project helped in:
- Understanding Django framework architecture
- Implementing custom user authentication
- Working with Django models and migrations
- Creating responsive web interfaces
- Managing project workflows and version control
- Team collaboration and code review

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

Run tests with:
```bash
python manage.py test
```

For production deployment, ensure proper security configurations including debug mode deactivation, allowed hosts setup, secure email backends, production databases, static file serving, and HTTPS implementation. Optional Docker containerization is also supported for streamlined deployment.

The project is licensed under the MIT License, promoting open collaboration and reuse.

We extend our heartfelt gratitude to Mr. Anshuman Rajkonwar for his invaluable guidance and mentorship throughout the internship at APDCL Bijulee Bhawan. Special recognition goes to Assam Kaziranga University for providing the academic foundation, and to team member Rittik Das for the collaborative development journey. This endeavor celebrates the synergy of academic learning and practical application in computer science.

For inquiries or feedback about this internship project, please connect through appropriate professional channels.

This initiative represents the successful completion of a transformative one-month internship experience at APDCL Bijulee Bhawan, seamlessly integrating academic knowledge with real-world software development.
