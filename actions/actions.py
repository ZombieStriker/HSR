class AAction:
    def __init__(self, name):
        self.name = name

    def setParameters(self, params):
        self.params = params

    def action(self, databall, currentContext,actiondataball):
        print("Firing "+self.name)
