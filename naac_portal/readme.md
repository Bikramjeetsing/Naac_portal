 NAAC Portal

 Overview

The NAAC Portal is a Djangobased web application designed for managing accreditation data. It allows users to upload, organize, and retrieve yearly documentation across 7 chapters, each with different numbers of subchapters  whch have each different number of categories. The system ensures secure access, dynamic content display, and automated background tasks.

 Features

 User Authentication & Access Control

   Users can only access their updateation chapter
   Admins can manage users and content

 Document Management

   Upload PDFs for specific chapters & years
   Retrieve and view uploaded PDFs

 Dynamic Content Display

   Chapters & subchapters load dynamically
   Yearly data carousel for better visualization

 Background Task Management (Celery & Django Celery Beat)

   Automated periodic tasks (e.g., data updates, report generation)
   Task scheduling with Django Celery Beat

 Notifications & Messaging (Twilio Integration)

   Automated notifications via SMS/email using Twilio

 Tech Stack

 Backend: Django, Celery, Django Celery Beat
 Frontend: HTML, JavaScript
 Database: SQLlite3
 Task Scheduling: Celery with Redis as broker
 Notifications: Twilio API for WhatsApp messages 

 Installation & Setup

 Prerequisites

 Python 3.9+
 Django
 Redis (for Celery)
 SQLlite3
 Twilio&x20;
 Celery
 Django\_Celery\_Beat

 Steps

1. Create a virtual environment and activate it:

   ```sh
   python m venv env
   source env/bin/activate   On Windows: env\Scripts\activate
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```sh
   python manage.py migrate
   ```

4. Start Redis (for Celery tasks):

   ```sh
   redisserver
   ```

5. Run Celery worker & Celery Beat:

   ```sh
   celery A naac_portal worker loglevel=info
   celery A naac_portal beat loglevel=info
   ```

6. Run the Django development server:

   ```sh
   python manage.py runserver
   ```

7. Access the portal:
   Open your browser and go to `http://127.0.0.1:8000`

 Usage

 Admin Panel: `http://127.0.0.1:8000/admin`
 Upload PDFs: Admins can upload documents categorized by year & chapter
 User Restrictions: Each user can only access their assigned chapter

 Future Enhancements

 Implement AIpowered document categorization
 Add RoleBased Access Control (RBAC)
 Improve UI with React or Vue.js

 License

This project is licensed under the MIT License.



 Contributors

 Arshdeep Singh (Lead Developer)

For any issues or feature requests, please raise a GitHub issue. 🚀

