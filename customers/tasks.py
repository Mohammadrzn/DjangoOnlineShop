from random import randint

from django.core.mail import send_mail
from celery import shared_task
import redis

redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


@shared_task
def send_otp_email(email):
    otp_code = randint(100000, 999999)
    print(otp_code)
    redis_instance.setex(email, 300, otp_code)
    send_mail(
        'Email Verification',
        f'Your OTP code is: {otp_code}',
        'mohammadbagherrezanejad@gmail.com',
        [email],
    )


@shared_task
def send_otp_sms(phone_number, exp_time):
    otp_code = randint(100000, 999999)
    print(otp_code)
    redis_instance.setex(phone_number, exp_time, otp_code)
