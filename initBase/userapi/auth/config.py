from .PT.pTEngines import MobilePTEngine, PTEnginesBase
from userapi.exception import CustomAPIX





class Config:
    REQUIRED_ON_Account_CREATION = None
    PTEngine = {
        "mobile_otp": MobilePTEngine
    }
 

        
    def getPTEngine(self, task_name, raise_exception=False):
        
        e = self.PTEngine.get(task_name, None)

        if raise_exception  and e is None:
            raise CustomAPIX({"detail": "Something went Wrong"}, server_error=True)
        

        if e is not None:
            return e
        return PTEnginesBase
        
    
    
    # ["mobile_verification", {
    #         "handler": ""
    #     }]
# # None | [['Mobile_verification', {"handler_class": ''}]] 