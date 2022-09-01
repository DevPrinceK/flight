# Flight Booking App
Backend services and api for a flight/trip booking application. This application contains the api (to be integrated to mobile apps) that enables one to book and filght, make payments, search for available flights/trips etc. It also contains the backend dashboard for the travel agencies and administrators of the system to manage the entire system. With the backend, admins and agencies can:  <br />
1. Manage agencies  <br />
  a. create agencies  <br />
  b. update agency details  <br />
  c. delete agencies  <br />
2. Manage vehicles  <br />
  a. create vehicles  <br />
  b. update vehicles  <br />
  c. delete vehicles  <br />
3. Manage Seats <br />
  a. create seats <br />
  b. update seats <br />
  c. delete seats <br />
4. Manage Vehicle Categories <br />
  a. create vehicle category <br />
  b. update vehicle category <br />
  c. delete vehicle category <br />
5. Manage Trips <br />
  a. create trips <br />
  b. update trips <br />
  c. delete trips <br /> 
6. Manage Bookings <br />
  a. view bookings made by end users <br />
7. Manage Transactions <br />
  a. View transactions going through the system <br />
8. Manage Tickets <br />
  a. view all system generated tickets <br />
  
# Languages / Frameworks
1. Python
2. Django
3. DjangoRestFramework
4. Django Knox

# Installation
1. Step One: <br />
Clone the repository <br />
```git clone https://github.com/DevPrinceK/flight.git```

2. Step 2 <br />
Navigate to project <br />
```cd ./flight```

3. Step 3 <br />
Create Virtual Environment <br />
```python -m venv venv```

4. Install dependencies <br />
Navigate to the core of the project <br />
```cd core``` <br />
Install dependencies from ```requirements.txt file```. <br />
```pip install requirements.txt``` <br />

5. Makemigrations <br />
After successful installation of dependencies, make migrations. <br />
```python manage.py makemigrations``` <br />

After making migrations, ensure to migrate your changes. <br />
```python manage.py migrate``` <br />

