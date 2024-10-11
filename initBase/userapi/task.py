from celery import shared_task
import time
from requests import request

@shared_task
def sendmailOtp():
    print("task start")
    
    print("task done")

@shared_task
def sendMobileOtp(otp, ph_number):
    time.sleep(5)
    ic(f"we sent successfully {otp} on {ph_number}")