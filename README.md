# Django Web Application

This is a Django-based web application designed for user authentication and email verification. Follow the steps below to set up and run the application.

## Features

- User registration with email verification.
- User login and logout.
- Email verification and password recovery functions
- Role-based access compatible

## Prerequisites

Make sure you have the following installed on your machine:

- Python (version 3.10 or higher recommended)
- pip (Python package installer)
- Virtualenv (optional but recommended for isolating dependencies) or pipenv

## Installation Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Step 2: Set Up a Virtual Environment

Create and activate a virtual environment:

#### Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Database

Apply migrations to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Application

### Step 1: Create a Superuser (Optional)

To access the Django admin interface, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin credentials.

### Step 2: Start the Development Server

Run the Django development server:

```bash
python manage.py runserver
```

The application will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Using the Application

- **User Registration:** Navigate to `/signup/` to register a new account.
- **Email Verification:** Check your email for a verification link to activate your account.
- **Login:** Navigate to `/login/` to log in with your credentials.

## Additional Notes

- The app uses a SQLite database by default. To switch to another database (e.g., PostgreSQL), update the `DATABASES` setting in `settings.py`.
- Use the `DEBUG` setting in `settings.py` appropriately for development (`DEBUG=True`) and production (`DEBUG=False`).

## Contribution Guidelines

1. **Fork the repository.**
2. **Create a feature branch:**

   ```bash
   git checkout -b feature-name
   ```

3. **Commit your changes:**

   ```bash
   git commit -m "Add feature description"
   ```

4. **Push to the branch:**

   ```bash
   git push origin feature-name
   ```

5. **Open a pull request.**

## License

This project is licensed under the MIT License.

