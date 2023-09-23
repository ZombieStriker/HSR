from actions.actions import AAction

class ParseFactAction(AAction):
    def __init__(self,):
        super().__init__("ParseFact")


    def action(self,databall, currentContext, actiondataball):
        """Parses a fact about the object in \"memory1\""""
        if "memory1" in databall:
            ocurrence = databall["memory1"]["occurrence"]
            values = databall["memory1"]["values"]
            if not "connector" in databall["memory1"]:
                connector = "and"
            else:
                connector = databall["memory1"]["connector"]

            formatted_str = ocurrence+" "
            index = 0
            for i in values:
                if index == 0 and len(values)==1:
                    formatted_str+=i
                elif index == len(values)-1:
                    formatted_str+=connector+" "+i
                else:
                    formatted_str+=i+" "
                index=index+1

            databall["memory1"] = formatted_str

        else:
            databall["memory1"] = actiondataball.memory["NULL"]