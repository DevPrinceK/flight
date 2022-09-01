# Flight Booking App
Backend services and api for a flight/trip booking application. This application contains the api (to be integrated to mobile apps) that enables one to book and filght, make payments, search for available flights/trips etc. It also contains the backend dashboard for the travel agencies and administrators of the system to manage the entire system. With the backend, admins and agencies can:  <br />
1. Manage agencies  <br />
  a. create agencies  <br />
  b. update agency details  <br />
  c. delete agencies  <br />
 <br />  <br />
2. Manage vehicles  <br />
  a. create vehicles  <br />
  b. update vehicles  <br />
  c. delete vehicles  <br />
<br />
3. Manage Seats <br />
  a. create seats <br />
  b. update seats <br />
  c. delete seats <br />
<br />
4. Manage Vehicle Categories <br />
  a. create vehicle category <br />
  b. update vehicle category <br />
  c. delete vehicle category <br />
  
5. Manage Trips <br />
  a. create trips <br />
  b. update trips <br />
  c. delete trips <br /> <br />
  
6. Manage Bookings <br />
  a. view bookings made by end users <br /> <br />
  
7. Manage Transactions <br />
  a. View transactions going through the system <br /> <br />
  
8. Manage Tickets <br />
  a. view all system generated tickets <br /> <br />

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

