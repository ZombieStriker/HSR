from actions.actions import AAction

class AddSubProcessAction(AAction):
    def __init__(self,):
        super().__init__("AddSP")


    def action(self,databall, currentContext, actiondataball):
        """Adds a sub process to the stack of subprocesses"""
        if(len(self.params) > 0):
            for ss in actiondataball.SUBPROCESSES:
                if(ss.name == self.params[0]):
                    newparams = [len(self.params)-1]
                    for i in range(1,len(self.params)):
                            if self.params[i].startswith("&"):
                                self.params[i] = self.params[i][1:]
                                var_gross = -1
                                try:
                                      if "var_"+self.params[i] in databall:
                                           var_gross = databall["var_"+self.params[i]]
                                except:
                                    print("Failed to find "+self.params[i])
                                
                                if var_gross>=0:
                                    stringname = currentContext[var_gross].text
                                    stringtemp = ""
                                    for i in range(0,len(stringname)):
                                        stringtemp=stringtemp.join(stringname[i])
                                        if i < len(stringname)-1:
                                           stringtemp=stringtemp.join("_")
                                    if stringtemp in actiondataball.memory:
                                        newparams[i-1] = actiondataball.memory[stringtemp]["name"]
                            else:
                                newparams[i-1]=self.params[i]
                    
                    ss.setParameters(newparams)
                    actiondataball.subprocesses.append(ss)
                    return
            
