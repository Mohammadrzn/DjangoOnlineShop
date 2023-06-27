# Django Online Shop

## Introduction
An online shop with python and django. Customers can access site, add products to cart and see cart but for the payment, they should login
Default login method is with user and password and it works with JWT, but they can use OTP code with email or mobile number
Customers can have default address and can select between addresses on payment
Categories and products can have discounts

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

## Setup
First set an virtual environment:
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
