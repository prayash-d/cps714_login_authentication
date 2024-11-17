Django Web Application

This is a Django-based web application designed for user authentication and email verification. Follow the steps below to set up and run the application.

Features

User registration with email verification.

User login and logout.

Custom user model using email instead of username.

Prerequisites

Make sure you have the following installed on your machine:

Python (version 3.10 or higher recommended)

pip (Python package installer)

Virtualenv (optional but recommended for isolating dependencies)

Installation Instructions

Step 1: Clone the Repository

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

Windows:

python -m venv env
env\Scripts\activate

macOS/Linux:

python3 -m venv env
source env/bin/activate

Step 3: Install Dependencies

Install the required Python packages using the requirements.txt file:

pip install -r requirements.txt

Step 4: Configure the Database

Apply migrations to set up the database:

python manage.py makemigrations
python manage.py migrate

Running the Application

Step 1: Create a Superuser (Optional)

To access the Django admin interface, create a superuser:

python manage.py createsuperuser

Follow the prompts to set up the admin credentials.

Step 2: Start the Development Server

Run the Django development server:

python manage.py runserver

The application will be accessible at http://127.0.0.1:8000/.

Using the Application

User Registration: Navigate to /signup/ to register a new account.

Email Verification: Check your email for a verification link to activate your account.

Login: Navigate to /login/ to log in with your credentials.

Additional Notes

The app uses a SQLite database by default. To switch to another database (e.g., PostgreSQL), update the DATABASES setting in settings.py.

Use the DEBUG setting in settings.py appropriately for development (DEBUG=True) and production (DEBUG=False).

Contribution Guidelines

Fork the repository.

Create a feature branch:

git checkout -b feature-name

Commit your changes:

git commit -m "Add feature description"

Push to the branch:

git push origin feature-name

Open a pull request.

License

This project is licensed under the MIT License.

