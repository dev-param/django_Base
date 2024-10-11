from django.test import TestCase
from rest_framework.test import APIClient
import json

# Create your tests here.


factory = APIClient()

test = factory.post("/login/", json.dumps({
    "username": "waheguru",
    "password": "waheguru"
}), content_type='application/json')
ic(

    test
)