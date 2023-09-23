from actions.actions import AAction
import random

class ParseSegmentAction(AAction):
    def __init__(self,):
        super().__init__("Parse")


    def action(self,databall, currentContext,actiondataball):
        var_gross = -1

        try:
            if "var_"+self.params[0] in databall:
                var_gross = databall["var_"+self.params[0]]
        except:
            print("Failed to find "+self.params[0])


        if var_gross>=0:
            lenth = 1
            if "varlen_"+self.params[0] in databall:
                lenth = int(databall["varlen_"+self.params[0]])
            j = 0
            words = []
            while j < lenth:
                if(len(currentContext) <= var_gross+j):
                    print("Gross+J = "+str(var_gross+j) +" is greater than allowed (<"+str(len(currentContext))+")")
                    break
                stringname = currentContext[var_gross+j].text
                words.append(stringname)
                j+=1

            cc = currentContext[var_gross:var_gross+lenth]
            parsed = actiondataball.parsemethod(words,cc)

            
            if len(parsed) == 0:
                return
            value = parsed[random.randint(0,len(parsed)-1)]
            selectedSentence = value["jj"]
            print(str(databall["deep"])+":="+"Found sub-sentence structure : "+str(selectedSentence["input"]))


            cctext = ""
            for c in cc:
                for ccc in c.text:
                    cctext=cctext+" "+ccc

            print(str(databall["deep"])+":="+" For text: "+cctext)


            stack=[]
            tdataball = {}
            for d in databall:
                if not d.startswith("var_") and not d.startswith("varlen_") and  d !="actionindex" and d != "output" and d != "deep":
                    tdataball[d] = databall[d]

            for action in selectedSentence["stack"]:
                stack.append(action)
            for k in value["databall"]:
                tdataball[k]=value["databall"][k]
            
            tdataball["deep"] = databall["deep"]+1
            for actionraw in stack:
                actionsplit = actionraw.split(":",1)
                actionname = actionsplit[0]
                parametersraw=actionsplit[1]
                params = []
                for i in range(0,parametersraw.count(":")+1):
                    split = parametersraw.split(":",1)
                    params.append(split[0])
                    if len(split)>1:
                        parametersraw=split[1]

                for a in actiondataball.ACTIONS:
                    if a.name == actionname:
                        a.setParameters(params)
                        a.action(tdataball,cc,actiondataball)
                





                for d in tdataball:
                    if not d.startswith("var_") and not d.startswith("varlen_") and  d !="actionindex" and d != "output" and d != "deep":
                        databall[d]=tdataball[d]
                        print(str(databall["deep"])+":="+"Transferring "+d +" " + str(databall[d]))


        else:
            print("Cannot find "+str(var_gross)+" (var_"+self.params[0]+")")