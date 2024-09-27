# Air-Reserve
Air Reserve is an application that allows passengers to book seats on flights out of Entebbe International Airport.

# Features
1. Flight Search: Users can search for flights based on their preffered dates, destinations and other criteria.

2. Reservation Management: Once a flight is booked, users can easily make and manage their reservations , including seat reservations.

3. Admin Dashboard: The airline has access to a comprehensive admin dashboard where they can manage flights , view reservations, and monitor user activity.

# Installation
To setup airReserve on your system, follow the following instructions

1. Clone the repository
git clone https://github.com/fatuma65/Air-Reserve.git

2. Navigate to the project directory 
cd reserve

3. Actiavte your virtual environment
myenv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Set Up Database
 - Configure your database settings in your .env file
 - Run the migrations to create the neccessary tables

 py manage.py migrate

6. Start the Server
py manage.py runserver

7. Access airReserve in your web browser at 
http://127.0.0.1:8000/