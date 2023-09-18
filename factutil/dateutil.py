from datetime import date, timedelta
import calendar

class DateUtil:
    def __init__(self) -> None:
        pass

    def getDayOfWeekFromRelative(self, strDate):
        today = date.today()
        if(strDate == "today" or strDate == "todays"):
            d2 = calendar.day_name[today.weekday()]
            return d2
        if(strDate == "yesterday"or strDate == "yesterdays"):
            yesterday = today - timedelta(days=1)
            d2 = calendar.day_name[yesterday.weekday()]
            return d2
        if(strDate == "tomorrow"or strDate == "tomorrows"):
            tomorrow = today + timedelta(days=1)
            d2 = calendar.day_name[tomorrow.weekday()]
            return d2

    def getDateFromRelative(self, strDate):
        today = date.today()
        if(strDate == "today"or strDate == "todays"):
            d2 = today.strftime("%B %d, %Y")
            return d2
        if(strDate == "yesterday"or strDate == "yesterdays"):
            yesterday = today - timedelta(days=1)
            d2 = yesterday.strftime("%B %d, %Y")
            return d2
        if(strDate == "tomorrow"or strDate == "tomorrows"):
            tomorrow = today + timedelta(days=1)
            d2 = tomorrow.strftime("%B %d, %Y")
            return d2