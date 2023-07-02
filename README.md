# Django Online Shop


## Introduction
An online shop with python and django. Customers can access site, add products to cart and see cart but for the payment, they should log in
Default login method is with user and password, and it works with JWT, but they can use OTP code with email or mobile number
Customers can have default address and can select between addresses on payment
Categories and products can have discounts


## Some features of project
* models Unittest
* debug and info log levels (writen on file and terminal)
* JWT authentication
* OTP code authentication via Email and phone number


## Technologies
* celer: 5.2.7
* cryptography: 40.0.2
* Django: 4.2.1
* django-admin-persian-fonts: 0.2
* django-jalali-date: 1.0.2
* django-templated-mail: 1.1.1
* djangorestframework: 3.14.0
* djangorestframework-simplejwt: 5.2.2
* Pillow: 9.5.0
* PyJWT: 2.7.0
* pytz: 2023.3
* redis: 4.5.5

  for more see requirements.txt


## Setup (with Docker)
First create a docker image:
```
docker build -t django-online-shop .
```
Check if the image created successfully (you should see the image named django-online-shop):
```
docker image ls
```
Run the project via docker:
```
docker run django-online-shop
```


## Setup (without Docker)
First create a virtual environment:
```
python3 -m venv venv
```
Activate the virtual environment:
```
source venv/bin/activate
```
Then install requirements from requirements.txt:
```
pip install -r requirements.txt
```
Make migrations to create python codes for creating database from models.py:
```
python manage.py makemigrations
```
Create data base from migration files:
```
python manage.py migrate
```
Create superuser for online shop:
```
python manage.py createsuperuser
```
Run the project:
```
python manage.py runserver
```
In a second terminal run this to install redis tools (we are going to use it as a message broker to send OTP codes)
```
sudo apt install redis-tools
```
Then install redis server
```
sudo apt install redis-server
```
First run redis server
```
redis-server
```
And then redis cli (If everything is okay, when you write "ping" in redis terminal it should return "PONG")
```
redis-cli
```
In a third terminal this command to activate celery
```
python -m celery -A customers worker -l info
```

now go to http://127.0.0.1:8000/ and enjoy the shop
