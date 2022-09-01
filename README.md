# Flight Booking App
Backend services and api for a flight/trip booking application. This application contains the api (to be integrated to mobile apps) that enables one to book and filght, make payments, search for available flights/trips etc. It also contains the backend dashboard for the travel agencies and administrators of the system to manage the entire system. With the backend, admins and agencies can:
1. Manage agencies
  a. create agencies
  b. update agency details
  c. delete agencies
  
2. Manage vehicles
  a. create vehicles
  b. update vehicles
  c. delete vehicles

3. Manage Seats
  a. create seats
  b. update seats
  c. delete seats
  
4. Manage Vehicle Categories
  a. create vehicle category
  b. update vehicle category
  c. delete vehicle category
  
5. Manage Trips
  a. create trips
  b. update trips
  c. delete trips
  
6. Manage Bookings
  a. view bookings made by end users
  
7. Manage Transactions
  a. View transactions going through the system
  
8. Manage Tickets
  a. view all system generated tickets

# Stack
1. Django
2. DjangoRestFramework
3. Django Knox

# Installation
1. Step One:
Clone the repository
```git clone https://github.com/DevPrinceK/flight.git```

2. Step 2
Navigate to project
```cd ./flight```

3. Step 3
Create Virtual Environment
```python -m venv venv```

4. Install dependencies
Navigate to the core of the project
```cd core```
Install dependencies from ```requirements.txt file```.
```pip install requirements.txt```

5. Makemigrations
After successful installation of dependencies, make migrations.
```python manage.py makemigrations```

After making migrations, ensure to migrate your changes.
```python manage.py migrate```

