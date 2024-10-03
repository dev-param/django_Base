from celery import shared_task
import time
from requests import request

@shared_task
def sendmailOtp():
    print("task start")
    
    print("task done")
