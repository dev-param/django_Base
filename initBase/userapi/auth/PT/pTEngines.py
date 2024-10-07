class PTEnginesBase:
    def __init__(self, user):
        self.user = user



    def send(self, data):
        ic("This is just debug testing you Make Your Own class")
        ic(f"for debugging code is: {data}")


class MobilePTEngine(PTEnginesBase):
    def send(self, data):
        ic(self.user.mobile_number)
        