class AAction:
    def __init__(self, name):
        self.name = name

    def setParameters(self, params):
        for i in range(0,len(params)):
            if(i==0):
                self.p1=params[i]
            if(i==1):
                self.p2=params[i]
            if(i==2):
                self.p3=params[i]
            if(i==3):
                self.p4=params[i]
            if(i==4):
                self.p5=params[i]

    def action(self, databall, currentContext, memory, tts, speak):
        print("Firing "+self.names)
