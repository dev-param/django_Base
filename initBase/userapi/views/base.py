
# drf
from rest_framework.views import APIView


import json

# Create your views here.




class MainAPIView(APIView):
    def parseError(self, exceptionClass, strDetails="Something Wrong", jsonDetails={}):
        return exceptionClass({
            "detail": strDetails,
            "JsonInfo": json.loads(str(jsonDetails))
        })

