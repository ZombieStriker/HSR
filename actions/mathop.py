from actions.actions import AAction

class MathOpAction(AAction):
    def __init__(self,):
        super().__init__("Math")


    def action(self,databall, currentContext,actiondataball):
        """Performs arithmatic on \"memory1\" and sets memory1 to the new value"""
        if "memory1" in databall:
            var_gross = -1
            try:
                if "var_"+self.params[0] in databall:
                    var_gross = databall["var_"+self.params[0]]
            except:
                print("Failed to find "+self.params[0])

                
            var_gross2 = -1
            try:
                if "var_"+self.params[1] in databall:
                    var_gross2 = databall["var_"+self.params[1]]
            except:
                print("Failed to find "+self.params[1])

            if(var_gross == -1 or var_gross2 == -1):
                return

            if(var_gross >= len(currentContext) or var_gross2 >= len(currentContext)):
                return

            operator = currentContext[var_gross]
            othernumber = currentContext[var_gross2]


            isnumber1 = False
            print("Databall is "+str(databall["memory1"]))
            for k in databall["memory1"]["tags"]:
                if k =="NUMBER":
                    isnumber1=True
                    break
            isnumber2 = False
            for k in othernumber.tags:
                if k =="NUMBER":
                    isnumber2=True
                    break
            isop = False
            for k in operator.tags:
                if k =="MATH_OP":
                    isop=True
                    break


            math = 0
            if(isnumber1 and isnumber2 and isop):

                otherNumValue = -1
                try:
                    otherNumValue = int(othernumber.number)
                except:
                    otherNumValue = int(othernumber.meaning["number"])

                if(hasTag(operator,"MATH_OP_PLUS")):
                    math = int(databall["memory1"]["number"]) + otherNumValue
                if(hasTag(operator,"MATH_OP_SUB")):
                    math = int(databall["memory1"]["number"]) - otherNumValue
                if(hasTag(operator,"MATH_OP_DIV")):
                    math = int(databall["memory1"]["number"]) / otherNumValue
                if(hasTag(operator,"MATH_OP_MUL")):
                    math = int(databall["memory1"]["number"]) * otherNumValue

            databall["memory1"] = {
                "name":math,
                "tags":["NUMBER"],
                "number":math
            }
            
                

def hasTag(context, tagname):
    for tag in context.tags:
        if tag == tagname:
            return True
    return False