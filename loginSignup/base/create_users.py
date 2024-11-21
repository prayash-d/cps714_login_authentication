from .models import CustomUser, UserProfile
import random

# Sample data for creating users
roles = ['Admin', 'Retailer', 'Customer', 'Partner']
first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Helen', 'Ivy', 'Jack']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Martinez', 'Wilson']
contact_numbers = ['1234567890', '2345678901', '3456789012', '4567890123', '5678901234', '6789012345', '7890123456', '8901234567', '9012345678', '0123456789']

# Function to create 10 users
def create_users():
    for i in range(10):
        email = f"user{i+1}@example.com"
        password = f"password{i+1}"
        role = random.choice(roles)
        first_name = first_names[i]
        last_name = last_names[i]
        contact_number = contact_numbers[i]

        # Create a new CustomUser
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            role=role
        )

        # Create a UserProfile associated with this CustomUser
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number
        )
        print(f"Created user: {email} with role: {role}")

# Call the function to create users
create_users()
