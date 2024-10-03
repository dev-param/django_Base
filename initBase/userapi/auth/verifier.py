from rest_framework import exceptions
# date 
from django.utils import timezone
from datetime import timedelta
# local
from userapi.models import LogsModel


def checkIfAllowed(user):
    """ raise exception if something went wrong """
    logModel = LogsModel.loginFailedLog(user)
    
    if isTimeBlocked(logModel):
        raise exceptions.PermissionDenied({"detail": "Account Temporarily Banned"})
    







def isTimeBlocked(model,
                   callback=lambda model:isTimeBlocked(model, None, base_time=timezone.now() - timedelta(minutes=15), max_BT=3),
                **kwargs
                ):
    """
   

    **kwargs default

        base_time=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0),\n
        max_BT=20, # max try in base_time
        \n



    if user blocked for some time 
        return True
    else
        return False
    """
    baseTime = kwargs.get("base_time", timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
    max_BT= kwargs.get("max_BT", 20)

  
    model1 = model.filter(_at__gt=baseTime)
    print(model1)

    if not model1.exists():
        return False
    
    if model1.count() > max_BT:
        return True
    
    if callback is not None:
        return callback(model1)
    else:
        return False
    









def LoginLog(user):
    return LogsModel.loginFailedLog(user, create=True, _info={})
