from actions.actions import AAction
from factutil.dateutil import DateUtil

class LookUpDateAction(AAction):
    def __init__(self,):
        super().__init__("LookUpDate")


    def action(self,databall, currentContext, memory, tts, speak):
        if "memory1" in databall and "name" in databall["memory1"]:
            relDate = databall["memory1"]["name"]
            date = DateUtil().getDateFromRelative(relDate)
            databall["memory1"] = date
        else:
            databall["memory1"] = memory["NULL"]